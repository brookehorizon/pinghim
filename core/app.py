import tkinter as tk
from core.isconnected import IsConnected
from core.settings import  *
import os
from datetime import datetime
from scapy.all import srp,Ether,ARP,conf 

    

class App:
    def ping(self):
        if IsConnected(self.e1.get()).isconnected():
            on_conn()
            self.zenity(msg=f"{self.e1.get()} is connected !")


    def notify(self, msg, **kwargs):
        os.system(f'notify-send -u low "{msg}" ')

    def zenity(self, msg, **kwargs):
        os.system(f'zenity --info --title="Show All" --text="{msg}" --no-wrap')


    def Show_All(self, interface=interface, ips=ips):
        
        start_time = datetime.now()

        conf.verb = 0 
        try:
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = ips), 
                    timeout = 2, 
                    iface = interface,
                    inter = 0.1)
        except:
            self.notify(msg="Permission Error")
            


        output = "\n IP - MAC\n"
        for snd,rcv in ans: 
            output += rcv.sprintf(r"%ARP.psrc% - %Ether.src%\n")
        stop_time = datetime.now()
        total_time = stop_time - start_time 
        output += f"\n[*] Scan Complete. Duration: {total_time}"
        os.system(f'zenity --info --title="Show All" --text="{output}" --no-wrap')

    def run_app(self):
        master = tk.Tk()
        master.title("PingHim")
        tk.Label(master, text="ip").grid(row=0)
        master.geometry('400x150')


        self.e1 = tk.Entry(master)

        self.e1.insert(10, "127.0.0.1")

        self.e1.grid(row=0, column=1)

        tk.Button(master,
                text='Quit', 
                command=master.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Run', command=self.ping).grid(row=3, column=1,  sticky=tk.W, pady=4)
        tk.Button(master, text='Show All', command=self.Show_All).grid(row=3, column=2,  sticky=tk.W, pady=4)

        master.mainloop()


if __name__ == '__main__':
    App().run_app()
