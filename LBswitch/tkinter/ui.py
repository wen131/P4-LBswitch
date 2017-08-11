from tkinter import *
from scapy.all import *
import os
import threading

CLI_PATH='/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json'

def do_cmd(CMD):
    os.system('echo %s | %s'%(CMD,CLI_PATH))


class Application(Frame):

    def change_image(self,k):
        self.label.configure(image=self.bms[k])
   
    def data_plane(self):
        sniff(iface = "veth11",
             prn = lambda x: self.handle_pkt(x))

    def createWidgets(self):
        self.btn_QUIT = Button(self)
        self.btn_QUIT["text"] = "QUIT"
        self.btn_QUIT["fg"]   = "red"
        self.btn_QUIT["command"] =  self.quit
        
        self.btn_QUIT.pack({"side":"left"})
        
        self.btn_addone = Button(self)
        self.btn_addone["text"] = "Add one"
        self.btn_addone["command"] = lambda : self.change_image(1)
        
        self.btn_addone.pack({"side":"left"})
        
        self.btn_update = Button(self)
        self.btn_update["text"] = "update weight"
        self.btn_update["command"] = lambda : self.change_image(2)

        self.btn_update.pack({"side":"right"})

        self.label= Label(image=self.bms[0])
        self.label.pack()

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



    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.bms=[PhotoImage(file='DIP%d.gif'%(i,)) for i in range(5)]
        self.createWidgets()
        self.hash_const=6
        self.hashes=[]
        self.weights=[2,0,1,1,0,2]
        self.VER=0
        self.t1=threading.Thread(target=self.data_plane)
        self.t1.start()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

