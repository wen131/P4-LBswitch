import wx
from scapy.all import *
import os
import threading

CLI_PATH='/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json'

def do_cmd(CMD):
    os.system('echo %s | %s'%(CMD,CLI_PATH))

class MyFrame(wx.Frame):  
  
    def __init__(self):  
        wx.Frame.__init__(self, parent=None,title="Controller",pos = (0,0), size=(1024,768))  
          
        self.Centre() 
        self.Show(True)

    
    def change_image(self,k):
        self.label.configure(image=self.bms[k])

    def data_plane(self):
        sniff(iface = "veth11",
             prn = lambda x: self.handle_pkt(x))

    def load_weights(self, args):
        self.VER+=1
        f=open('temp_commands.txt','w')
        i=0
        for arg in args:
            f.write('table_add route_table select_dip %d %d => %d\n'%(i,self.VER,arg))
            i+=1
        f.write('register_write version_register 0 %d\n'%(self.VER,))
        f.close()
        os.system('%s < %s'%(CLI_PATH, 'temp_commands.txt'))

    def update_DIPs(self):
        self.bms=[PhotoImage(file='DIP%d.gif'%(i,)) for i in range(5)]
        self.change_image(0)

    def update_DIPs(self):
        self.bms=[PhotoImage(file='DIP%d.gif'%(i,)) for i in range(5)]
        self.change_image(0)

    def update_weights(self):
        temp=[int(x)-1 for x in self.text_weights.get().split(" ")]
        self.load_weights(temp)
        self.weights=temp

    def OnMyButtonClick(self,event):
        self.btn.SetLabel("You Clicked!")  
          
    def OnQuit(self, event):
        self.Close()  
          

    def handle_pkt(self, pkt):
        if IP in pkt and TCP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            proto = pkt[IP].proto
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            id_tup = (src_ip, dst_ip, proto, sport, dport)
            res_dst=bytes(pkt)[:6]
            res_src=bytes(pkt)[6:12]
            if int.from_bytes(res_src,byteorder='big')==723:
                hash_res=int.from_bytes(res_dst,byteorder='big')
                if not (hash_res in self.hashes):
                    self.hashes.append(hash_res)
                    CMD="'table_add version_table select_version %d => %d'"%(hash_res,self.VER)
                    do_cmd(CMD)
                self.change_image(self.weights[hash_res%self.hash_const]+1)


if __name__ == '__main__':  
    app = wx.App()  
    frame = MyFrame()  
    app.MainLoop() 
