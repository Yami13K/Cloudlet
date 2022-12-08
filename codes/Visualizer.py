# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 19:38:41 2021

@author: Eng.MohammadSakka
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
class Visualizer:
    labelsSize = 5
    titleSize = 5
    legenSize = 5
    #%%  constructor
    def __init__(self):
        self.__fig = plt.figure()
        self.__grid = plt.GridSpec(5, 2, wspace=0.3, hspace=1)
        self.closed = False
        self.toClose = False
        self.__ax = plt.axes([0, 0, 0.1, 0.1])
        self.__button = Button(self.__ax,'exit')
        self.figlegend = plt.figure(figsize=(5,5))
        self.__grid2 = plt.GridSpec(5, 1, wspace=0.3, hspace=1)
        #self.__pauseResumeButton = RadioButtons(self.__ax2, ['pause', 'resume'],
                   #  [False,True],
                    # activecolor='r')
        #self.fig.subplots_adjust(hspace=.5)
    # functions
    #%% function visualizeMap
    def visualizeMap(self,areaDims):
        plt.figure(self.__fig.number)
        plt.subplot(self.__grid[0:,1])
        plt.xlim(0,areaDims[0])
        plt.ylim(0,areaDims[1])
        
        #%% function visualizeBSsGraph
    def visualizeBSsGraph(self,allBSs,BSsGraph):
        plt.figure(self.__fig.number)
        plt.subplot(self.__grid[0:,1])

        # visualize BSs
        for bs in allBSs:
            plt.plot(bs.getLocation()[0],bs.getLocation()[1],'ks', linewidth=2, markersize=12)
        
        # visualize BSs links
        for bs in allBSs:
            assosiatedBSsIds = bs.getAssosiatedBSsIds()
            for asBsId in assosiatedBSsIds[0]:
                plt.plot((bs.getLocation()[0],allBSs[asBsId].getLocation()[0]),
                         (bs.getLocation()[1],allBSs[asBsId].getLocation()[1]),
                          'b-.',alpha=0.05)
    #%% function visualizeUsers
    def visualizeUsers(self,users):
        plt.figure(self.__fig.number)
        plt.subplot(self.__grid[0:,1])
        for u in users:
            hl, = plt.plot(u.getLocation()[0],u.getLocation()[1],'g*',alpha=0.5)
            return hl
   #%% function visualizeCloudelets
    def visualizeCloudelets(self,allBSs):
        plt.figure(self.__fig.number)
        plt.subplot(self.__grid[0:,1])
        for bs in allBSs:
            if bs.getIsBScloudelet()==1:
                plt.plot(bs.getLocation()[0],bs.getLocation()[1],'r.', linewidth=2, markersize=10)
    #%% function visSystem
    # visualize the all system
    def visSystem(self,wman):
        # visualize the map
      
        
        areaDims = wman.getAreaDims()
        self.visualizeMap(areaDims)
        # visualize the base Stations
        allBSs = wman.getBSs()
        BSsGraph = wman.getBSsGraph()
        self.visualizeBSsGraph(allBSs,BSsGraph)
        # visualize the cloudelets
        self.visualizeCloudelets(allBSs)
        # visualize the users
        hl = self.visualizeUsers(wman.getUsers())

        # set legends
        plt.plot([],'g*',label='user')
        plt.plot([],'ks',label='base station')
        plt.plot([],'b-.',label='wire link')
        plt.plot([],'r.',markersize=5,label='cloudlet')
        
        plt.legend(loc ="upper left")

        
        return hl
 
    def exitVisualization(self,event):
        self.closed = True
        plt.close(self.__fig)
        plt.close(self.figlegend)
       # self.__fig = []
    #%% function updateUsersVisualization
    def updateUsersVisualization(self,users,hl):
        new_datax = []
        new_datay = []
        for u in users:
            loc = u.getLocation()
            new_datax.append(loc[0])
            new_datay.append(loc[1])
          
        hl.set_xdata(new_datax)
        hl.set_ydata(new_datay)
        self.__fig.canvas.draw()
   
        self.__fig.canvas.flush_events()
        #time.sleep(0.01)
    #%% function visualizeTasksServingMeasures
    def visualizeTasksServingMeasures(self,performanceLogger):
        plt.figure(self.__fig.number)
        ax = plt.subplot(self.__grid[1,0])
        ax.clear()
   
        STR = performanceLogger.getSTR_TS()
        RTR = performanceLogger.getRTR_TS()
        plt.plot(STR,'g.', label='locally served tasks ratio')
        plt.plot(RTR,'r.', label='remotely served tasks ratio')
        
        plt.title('tasks serving measures',fontsize=self.titleSize)
        plt.xlabel('time [sec]')
        plt.ylabel('mesasure')
        plt.legend(prop={'size':5}, loc = 'upper left')
        ax.xaxis. label. set_size(self.labelsSize)
        ax.yaxis. label. set_size(self.labelsSize)
        lines = ax.lines
        
        plt.figure(self.figlegend.number)
        ax2 = plt.subplot(self.__grid2[1,0])
        ax2.legend(lines, ('locally served tasks ratio', 'remotely served tasks ratio')\
                   ,loc= 'upper left')
    #%% function visualizeTasksServingMeasures
    def visualizeEnergyConsMeasures(self,performanceLogger):
        plt.figure(self.__fig.number)
        ax = plt.subplot(self.__grid[3,0])
        ax.clear()
        labels = ['cloudlet execution energy consumption',\
                  'users execution energy consumption',\
                 'tasks transmission energy consumption',\
                     'total energy consumption']
        #EE = performanceLogger.getExecEnerg_TS()
        UEE = performanceLogger.getUserExecEnergy_TS()
        print(f'the value of UEE is {UEE}')

        SE = performanceLogger.getSendingEnerg_TS()
        TE = performanceLogger.getTotalEnerg_TS()
        #plt.plot(EE,'b-')
        plt.plot(SE,'r.',  label='tasks transmission energy consumption')
        plt.plot(UEE,'ko', label='users execution energy consumption')
        plt.plot(TE,'g:', label='total energy consumption')
        
        plt.title('energy consumption measures',fontsize=self.titleSize)
        plt.xlabel('time [sec]')
        plt.ylabel('energy [joul]')
        ax.xaxis. label. set_size(self.labelsSize)
        ax.yaxis. label. set_size(self.labelsSize)
        plt.legend(prop={'size': 5},  loc='upper left')

        lines = ax.lines
        plt.figure(self.figlegend.number)
        ax2 = plt.subplot(self.__grid2[3,0])
        ax2.legend(lines, (labels),fontsize=self.legenSize)
   #%% function visualizeArrivedTasksNumber
    def visualizeArrivedTasksNumber(self,performanceLogger):
        art = performanceLogger.getArrivedTasks_TS()
        plt.figure(self.__fig.number)
        ax = plt.subplot(self.__grid[0,0])
        ax.clear()
        
        plt.plot(art,'g.', label='the number of arrived tasks')
        plt.title('number of arrived tasks',fontsize=self.titleSize)
        plt.xlabel('time [sec]')
        plt.ylabel('number of tasks')
        ax.xaxis. label. set_size(self.labelsSize)
        ax.yaxis. label. set_size(self.labelsSize)
        plt.legend(prop={'size': 7}, loc='upper left')

        lines = ax.lines
        plt.figure(self.figlegend.number)
        ax2 = plt.subplot(self.__grid2[0,0])
        ax2.legend(lines, ('number of arrived tasks',), loc = 'upper left')
   #%% function visualizeArrivedTasksNumber
    def visualizeServersRenting(self,performanceLogger):
        sr = performanceLogger.getRenting_TS()
        plt.figure(self.__fig.number)
        ax = plt.subplot(self.__grid[4,0])
        ax.clear()
        
        plt.plot(sr, 'g.', label='renting')
        plt.title('servers renting rate',fontsize=self.titleSize)
        plt.xlabel('time [sec]')
        plt.ylabel('renting')
        plt.legend(prop={'size': 7}, loc = 'upper left')
        ax.xaxis. label. set_size(self.labelsSize)
        ax.yaxis. label. set_size(self.labelsSize)
       
        lines = ax.lines
        plt.figure(self.figlegend.number)
        ax2 = plt.subplot(self.__grid2[4,0])
        ax2.legend(lines, ('mean of servers renting',),loc = 'upper left')
     #%%  function visualizeTasksDelayMeasures
    def visualizeTasksDelayMeasures(self,performanceLogger):
        w,r,q,s,e = performanceLogger.getAllMeasures()
        srt = performanceLogger.getSRT_TS()
        plt.figure(self.__fig.number)
        ax = plt.subplot(self.__grid[2,0])
        ax.clear()
        plt.plot(srt, label='system response time')
        plt.plot(w, label='average wireless delay')
        plt.plot(r, label='average routing delay')
        plt.plot(q, label='average sending to cloud delay')
        plt.plot(s, label='average local execution delay')
        plt.plot(e)

        plt.title('tasks delay factors',fontsize=self.titleSize)
        
        plt.xlabel('time [sec]')
        plt.ylabel('delay [sec]')
        plt.autoscale()
        plt.legend(prop={'size': 4})
        ax.xaxis. label. set_size(self.labelsSize)
        ax.yaxis. label. set_size(self.labelsSize)
        
        lines = ax.lines
        plt.figure(self.figlegend.number)
        ax2 = plt.subplot(self.__grid2[2,0])
        ax2.legend(lines, ('system responce time',\
                          'average wireless delay',\
                              'average routing delay',\
                                 'average queuing delay',\
                                  'average sending to cloud delay',\
                                    'average local execution delay'  ),\
                   loc = 'upper left',fontsize = self.legenSize)
    #%% pauseResume
    # def pauseResume(self,label):
    #     if label=='pause':
    #         plt.pause(1)
        
    #%% function updateVisualization
    def updateVisualization(self,wman,hl):

        self.updateUsersVisualization(wman.getUsers(),hl)
        self.visualizeTasksServingMeasures(wman.getPerformanceLogger())
        self.visualizeArrivedTasksNumber(wman.getPerformanceLogger())
        self.visualizeTasksDelayMeasures(wman.getPerformanceLogger())
        self.visualizeEnergyConsMeasures(wman.getPerformanceLogger())
        self.visualizeServersRenting(wman.getPerformanceLogger())
        self.__button.on_clicked(self.exitVisualization)
        # self.__pauseResumeButton.on_clicked(self.pauseResume)
        # plt.autoscale()
        plt.close(self.figlegend)
        # manager = plt.get_current_fig_manager()
        # manager.resize(*manager.window.maxsize())

        plt.show()
        # if self.closed:
        # figures=[manager.canvas.figure for manager in plt._pylab_helpers.Gcf.get_all_fig_managers()]
        # print(len(figures))
        # for f in range(1,len(figures)):
        #     plt.close(figures[f])

#%% end 
