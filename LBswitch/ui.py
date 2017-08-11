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
        
    def update_weights(self):
        temp=[int(x)-1 for x in self.text_weights.get().split(" ")]
        self.load_weights(temp)
        self.weights=temp

    def createWidgets(self):
        self.label= Label(image=self.bms[0])

        self.btn_QUIT = Button(self)
        self.btn_QUIT["text"] = "QUIT"
        self.btn_QUIT["fg"]   = "red"
        self.btn_QUIT["command"] =  self.quit
         
        
        self.btn_addone = Button(self)
        self.btn_addone["text"] = "Add one"
        self.btn_addone["command"] = self.update_DIPs
        
        
        self.btn_update = Button(self)
        self.btn_update["text"] = "update weight"
        self.btn_update["command"] = self.update_weights


        self.text_weights = Entry(self)
        self.text_weights.place(width=200,height=200,x=0,y=0)


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
        master.geometry('1024x768')
        self.bms=[PhotoImage(file='DIP3%d.gif'%(i,)) for i in range(4)]
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

