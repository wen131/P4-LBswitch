import wx
from matplotlib.figure import Figure  
import matplotlib.font_manager as font_manager  
import numpy as np  
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas  
# wxWidgets object ID for the timer  
TIMER_ID = wx.NewId()  
# number of data points  
POINTS = 50  
  
class PlotFigure(wx.Frame):  
    """Matplotlib wxFrame with animation effect"""  
    def __init__(self):  
        self.count=1
        wx.Frame.__init__(self, None, wx.ID_ANY, title="CPU Usage Monitor", size=(1280, 720))  
        # Matplotlib Figure  
        self.fig = Figure((16, 9), 80)  
        # bind the Figure to the backend specific canvas  
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)  
        # add a subplot  
        self.ax1 = self.fig.add_subplot(411) 
        self.ax2 = self.fig.add_subplot(412)
        self.ax3 = self.fig.add_subplot(413)
        self.ax4 = self.fig.add_subplot(414) 
        # limit the X and Y axes dimensions  
        self.ax1.set_ylim([-0.05, 1.2])  
        self.ax1.set_xlim([0, POINTS]) 

        self.ax2.set_ylim([-0.05, 1.2])  
        self.ax2.set_xlim([0, POINTS]) 

        self.ax3.set_ylim([-0.05, 1.2])  
        self.ax3.set_xlim([0, POINTS])

        self.ax4.set_ylim([-0.05, 1.2])  
        self.ax4.set_xlim([0, POINTS])
         
        self.ax1.set_autoscale_on(False)  
        self.ax1.set_xticks([])  

        self.ax2.set_autoscale_on(False)  
        self.ax2.set_xticks([]) 

        self.ax3.set_autoscale_on(False)  
        self.ax3.set_xticks([]) 

        self.ax4.set_autoscale_on(False)  
        self.ax4.set_xticks([]) 
        # we want a tick every 10 point on Y (101 is to have 10  
        self.ax1.set_yticks(range(0, 2, 10)) 
        self.ax2.set_yticks(range(0, 2, 10))
        self.ax3.set_yticks(range(0, 2, 10))
        self.ax4.set_yticks(range(0, 2, 10))
        # disable autoscale, since we don't want the Axes to ad  
        # draw a grid (it will be only for Y)  
        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax3.grid(True)  
        self.ax4.grid(True)
        # generates first "empty" plots  
        self.s1e = [None] * POINTS
        self.s1s = [None] * POINTS
        self.s1w = [None] * POINTS
        self.s2e = [None] * POINTS
        self.s2s = [None] * POINTS
        self.s2w = [None] * POINTS
        self.s3e = [None] * POINTS
        self.s3s = [None] * POINTS
        self.s3w = [None] * POINTS
        self.s4e = [None] * POINTS
        self.s4s = [None] * POINTS
        self.s4w = [None] * POINTS
 
        self.s1_e,=self.ax1.plot(range(POINTS),self.s1e,label='ECMP',linewidth=3) 
        self.s1_s,=self.ax1.plot(range(POINTS),self.s1s,label='STAT',linewidth=3)
        self.s1_w,=self.ax1.plot(range(POINTS),self.s1w,label='LBAS',linewidth=3) 

        self.s2_e,=self.ax2.plot(range(POINTS),self.s2e,label='ECMP %',linewidth=3) 
        self.s2_s,=self.ax2.plot(range(POINTS),self.s2s,label='STAT %',linewidth=3)
        self.s2_w,=self.ax2.plot(range(POINTS),self.s2w,label='WEIG %',linewidth=3)

        self.s3_e,=self.ax3.plot(range(POINTS),self.s3e,label='ECMP %',linewidth=3) 
        self.s3_s,=self.ax3.plot(range(POINTS),self.s3s,label='STAT %',linewidth=3)
        self.s3_w,=self.ax3.plot(range(POINTS),self.s3w,label='WEIG %',linewidth=3)

        self.s4_e,=self.ax4.plot(range(POINTS),self.s4e,label='ECMP %',linewidth=3) 
        self.s4_s,=self.ax4.plot(range(POINTS),self.s4s,label='STAT %',linewidth=3)
        self.s4_w,=self.ax4.plot(range(POINTS),self.s4w,label='WEIG %',linewidth=3)
        # add the legend  
        self.ax1.legend(loc='upper center', 
                           bbox_to_anchor=(0.5,1.5),
                           ncol=4,  
                           prop=font_manager.FontProperties(size=10))  
        # force a draw on the canvas()  
        # trick to show the grid and the legend  
        self.canvas.draw()  
        # save the clean background - everything but the line  
        # is drawn and saved in the pixel buffer background  
        self.bg1 = self.canvas.copy_from_bbox(self.ax1.bbox) 
        self.bg2 = self.canvas.copy_from_bbox(self.ax2.bbox)
        self.bg3 = self.canvas.copy_from_bbox(self.ax3.bbox)
        self.bg4 = self.canvas.copy_from_bbox(self.ax4.bbox)
        # bind events coming from timer with id = TIMER_ID  
        # to the onTimer callback function  
        self.timer = wx.Timer(self) 
        self.timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.onTimer,self.timer)
  
    def onTimer(self, evt):  
        """callback function for timer events"""  
        # restore the clean background, saved at the beginning
        if self.count<=46:
            self.count+=1
        else : self.timer.Stop() 
        self.canvas.restore_region(self.bg1)
        self.canvas.restore_region(self.bg2)
        self.canvas.restore_region(self.bg3)
        self.canvas.restore_region(self.bg4)  
        # update the data  
        with open('cpu_record_ecmp','r') as fecmp:
            dataecmp=fecmp.read().split("\n")[:-1]

        ecmp1=[s.split(" ")[0] for s in dataecmp]
        ecmp2=[s.split(" ")[1] for s in dataecmp]
        ecmp3=[s.split(" ")[2] for s in dataecmp]
        ecmp4=[s.split(" ")[3] for s in dataecmp]

        with open('cpu_record_static','r') as fstatic:
            datastatic=fstatic.read().split("\n")[:-1]

        static1=[s.split(" ")[0] for s in datastatic]
        static2=[s.split(" ")[1] for s in datastatic]
        static3=[s.split(" ")[2] for s in datastatic]
        static4=[s.split(" ")[3] for s in datastatic]

        with open('cpu_record_weight','r') as fweight:
            dataweight=fweight.read().split("\n")[:-1]

        weight1=[s.split(" ")[0] for s in dataweight]
        weight2=[s.split(" ")[1] for s in dataweight]
        weight3=[s.split(" ")[2] for s in dataweight]
        weight4=[s.split(" ")[3] for s in dataweight]
  
        self.s1e = self.s1e[1:] + [ecmp1[self.count]]
        self.s1s = self.s1s[1:] + [static1[self.count]]
        self.s1w = self.s1w[1:] + [weight1[self.count]] 
        self.s2e = self.s2e[1:] + [ecmp2[self.count]] 
        self.s2s = self.s2s[1:] + [static2[self.count]]
        self.s2w = self.s2w[1:] + [weight2[self.count]] 
        self.s3e = self.s3e[1:] + [ecmp3[self.count]] 
        self.s3s = self.s3s[1:] + [static3[self.count]]
        self.s3w = self.s3w[1:] + [weight3[self.count]] 
        self.s4e = self.s4e[1:] + [ecmp4[self.count]] 
        self.s4s = self.s4s[1:] + [static4[self.count]]
        self.s4w = self.s4w[1:] + [weight4[self.count]] 
        # update the plot  

        self.s1_e.set_ydata(self.s1e)
        self.s1_s.set_ydata(self.s1s)
        self.s1_w.set_ydata(self.s1w)
        self.s2_e.set_ydata(self.s2e)
        self.s2_s.set_ydata(self.s2s)
        self.s2_w.set_ydata(self.s2w)
        self.s3_e.set_ydata(self.s3e)
        self.s3_s.set_ydata(self.s3s)
        self.s3_w.set_ydata(self.s3w)
        self.s4_e.set_ydata(self.s4e)
        self.s4_s.set_ydata(self.s4s)
        self.s4_w.set_ydata(self.s4w)

        # just draw the "animated" objects  
        self.ax1.draw_artist(self.s1_e)
        self.ax1.draw_artist(self.s1_s)
        self.ax1.draw_artist(self.s1_w)

        self.ax2.draw_artist(self.s2_e)
        self.ax2.draw_artist(self.s2_s)
        self.ax2.draw_artist(self.s2_w)

        self.ax3.draw_artist(self.s3_e)
        self.ax3.draw_artist(self.s3_s)
        self.ax3.draw_artist(self.s3_w)

        self.ax4.draw_artist(self.s4_e)
        self.ax4.draw_artist(self.s4_s)
        self.ax4.draw_artist(self.s4_w)

        # It is used to efficiently update Axes data (axis ticks, labels, etc are not updated)  
        self.canvas.blit(self.ax1.bbox)
        self.canvas.blit(self.ax2.bbox)
        self.canvas.blit(self.ax3.bbox) 
        self.canvas.blit(self.ax4.bbox) 

if __name__ == '__main__':  

    app = wx.App()  
    frame = PlotFigure()  
    frame.Show()   
    app.MainLoop()

