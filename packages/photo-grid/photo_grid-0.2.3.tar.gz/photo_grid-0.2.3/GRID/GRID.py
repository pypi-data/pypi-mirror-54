# basic imports
import os
import sys
import warnings
warnings.filterwarnings("ignore")

# self imports
from .guser import *
from .gimage import *
from .gmap import *
from .gagent import *
from .lib import *

class GRID():
    """
    """

    def __init__(self):
        """
        ----------
        Parameters
        ----------
        """

        # self-defined class
        self.user = GUser()
        self.imgs = GImage()
        self.map = GMap()
        self.agents = GAgent()

        # for progressbar
        self.flag = True
        self.subflag = True
        self.window = 1000

    def __user__(self):
        """
        ----------
        Parameters
        ----------
        """

        self.user.printInfo()

    def run(self, pathImg=None, pathMap=None, pts=None,
            k=3, features=[0, 1, 2], lsSelect=[0], valShad=0, valSmth=0,
            nRow=0, nCol=0, nSmooth=100,
            tol=5, coefGrid=.2,
            outplot=False,
            path=None, prefix="GRID",
            preset=None):
        """
        ----------
        Parameters
        ----------
        """
        if preset is not None:
            params = getPickledGRID(preset)
            self.run(pathImg=pathImg, pathMap=pathMap, pts=pts, nSmooth=nSmooth, tol=tol,
                     **params, outplot=outplot)
        else:
            prog = initProgress(6, "loading data")
            self.loadData(pathImg=pathImg, pathMap=pathMap, outplot=outplot)
            prog = updateProgress(prog, 1, "cropping")
            self.cropImg(pts=pts, outplot=outplot)
            prog = updateProgress(prog, 1, "binarizing")
            self.binarizeImg(k=k, features=features,
                             lsSelect=lsSelect, valShad=valShad, valSmth=valSmth, outplot=outplot)
            prog = updateProgress(prog, 1, "locating plots")
            self.findPlots(nRow=nRow, nCol=nCol,
                           nSmooth=nSmooth, outplot=outplot)
            prog = updateProgress(prog, 1, "segmenting")
            self.cpuSeg(tol=tol, coefGrid=coefGrid, outplot=outplot)
            prog = updateProgress(prog, 1, "exporting")
            self.save(path=path, prefix=prefix)
            prog = updateProgress(prog, 1, "done!")

    def save(self, path=None, prefix="GRID"):
        """
        ----------
        Parameters
        ----------
        """
        if "__main__.py" not in sys.argv[0]:
            app = QApplication(sys.argv)

        self.savePlotAndDT(path=path, prefix=prefix)

        if "__main__.py" not in sys.argv[0]:
            app.quit()

        params = {
            "k" : self.imgs.paramKMs["k"],
            "features": self.imgs.paramKMs["features"],
            "lsSelect": self.imgs.paramKMs["lsSelect"],
            "valShad":  self.imgs.paramKMs["valShad"],
            "valSmth":  self.imgs.paramKMs["valSmth"],
            "nRow": self.agents.nRow,
            "nCol": self.agents.nCol,
            "coefGrid": self.agents.coef
        }

        try:
            pathOut = os.path.join(path, prefix) + ".grid"
            pickleGRID(params, pathOut)
        except:
            pathOut = os.path.join(self.user.dirHome, prefix) + ".grid"
            pickleGRID(params, pathOut)
        
    #=== === === === === === MAJOR WORKFLOW === === === === === ===

    def loadData(self, pathImg=None, pathMap=None, outplot=False):
        """
        ----------
        Parameters
        ----------
        """
        if pathImg is None:
            self.imgs.load(
                pathImg=os.path.join(self.user.dirGrid, "demo/seg_img.jpg"))
            self.map.load(
                pathMap=os.path.join(self.user.dirGrid, "demo/seg_map.csv"))
        else:
            self.imgs.load(pathImg=pathImg)
            self.map.load(pathMap=pathMap)
        
        if outplot:
            pltImShow(self.imgs.get("raw")[:,:,:3])

    def cropImg(self, pts=None, outplot=False):
        """
        ----------
        Parameters
        ----------
        """

        self.imgs.crop(pts)

        if outplot:
            pltImShow(self.imgs.get("crop")[:,:,:3])

    def binarizeImg(self, k=3, features=[0, 1, 2], lsSelect=[0], valShad=0, valSmth=0, outplot=False):
        """
        ----------
        Parameters
        ----------
        """
        # from QtCore import QTimer

        if self.imgs.get("crop") is None:
            self.cropImg()

        # KMEAN
        prog = None
        if self.flag:
            self.flag = False
            prog = initProgress(5, name="K-Means Clustering")
        self.imgs.doKMeans(k=k, features=features)
        # BINARIZE
        updateProgress(prog, name="Binarizing", flag=self.subflag)
        self.imgs.binarize(k=k, features=features, lsSelect=lsSelect)
        # SMOOTH
        updateProgress(prog, name="Smoothing", flag=self.subflag)
        self.imgs.smooth(value=valSmth)
        # DESHADOW
        updateProgress(prog, name="DeShade-ing", flag=self.subflag)
        self.imgs.deShadow(value=valShad)
        # FINALIZE
        updateProgress(prog, name="Finalizing", flag=self.subflag)
        self.imgs.finalized()
        updateProgress(prog, name="Done", flag=self.subflag)
        # set progress bar inactive for 300ms
        if self.subflag:     
            self.subflag = False
            QTimer.singleShot(self.window, lambda: setattr(self, "flag", True))
            QTimer.singleShot(self.window, lambda: setattr(self, "subflag", True))

        # Plot
        if outplot:
            pltImShowMulti(
                imgs=[self.imgs.get('crop')[:, :, :3], self.imgs.get(
                    'kmean'), self.imgs.get('binOrg'), self.imgs.get('bin')],
                titles=["Original", "K-Means", "Binarized", "Finalized"])

    def findPlots(self, nRow=0, nCol=0, nSmooth=100, outplot=False):
        """
        ----------
        Parameters
        ----------
        """

        # iamge 
        self.imgs.readyForSeg()

        self.map.findPlots(img=self.imgs.get("binSeg"),
                           nRow=nRow, nCol=nCol, nSmooth=nSmooth)

        self.agents.setup(gmap=self.map, img=self.imgs.get('binSeg'))
        
        if outplot:
            pltLinesPlot(gmap=self.map, agents=self.agents.agents, img=self.imgs.get('binSeg'))

    def cpuSeg(self, tol=5, coefGrid=.2, outplot=False):
        """
        ----------
        Parameters
        ----------
        """

        self.agents.cpuPreDim(tol=tol)
        self.agents.autoSeg(coefGrid=coefGrid)

        if outplot:
            pltSegPlot(self.agents, self.imgs.get("visSeg"), isRect=True)
        
    #=== === === === === === IMAGE === === === === === ===

    def rotateImg(self, nRot):
        """
        ----------
        Parameters
        ----------
        """
        self.imgs.rotate(nRot)

    #=== === === === === === MAP === === === === === ===

    def updateCenters(self, idx, angle=-1, nPeaks=0):
        if angle != -1:
            self.map.angles[idx] = angle
        if nPeaks != 0:
            self.map.nAxs[idx] = nPeaks
        self.map.locateCenters(img=self.imgs.get("binSeg"))
        self.map.nAxs[idx] = 0

    #=== === === === === === AGENTS === === === === === ===


    def fixSeg(self, width, length):
        """
        ----------
        Parameters
        ----------
        """
        self.agents.fixSeg(width, length)
  
    #=== === === === === === OUTPUT === === === === === ===

    def savePlotAndDT(self, path=None, prefix="GRID"):
        """
        ----------
        Parameters
        ----------
        """
        if path is None or not os.path.exists(path):
            path = self.user.dirHome

        # progress bar
        prog = initProgress(6+self.imgs.depth+5, "Exporting")

        # DF
        df = self.getDF()
        # NDVI
        idx = self.getDfIndex(ch_1=3, ch_2=0, isContrast=True, name_index="NDVI")
        df = pd.merge(df, idx, on='var', how='left')
        updateProgress(prog)
        # GNDVI
        idx = self.getDfIndex(
            ch_1=3, ch_2=1, isContrast=True, name_index="GNDVI")
        df = pd.merge(df, idx, on='var', how='left')
        updateProgress(prog)
        # NDGI
        idx = self.getDfIndex(
            ch_1=1, ch_2=0, isContrast=True, name_index="NDGI")
        df = pd.merge(df, idx, on='var', how='left')
        updateProgress(prog)
        # CNDVI
        idx = self.getDfIndex(ch_1=3, ch_2=0, ch_3=1,
                                isThree=True, name_index="CNDVI")
        df = pd.merge(df, idx, on='var', how='left')
        updateProgress(prog)
        # RVI
        idx = self.getDfIndex(ch_1=3, ch_2=0, isRatio=True, name_index="RVI")
        df = pd.merge(df, idx, on='var', how='left')
        updateProgress(prog)
        # GRVI
        idx = self.getDfIndex(ch_1=3, ch_2=1, isRatio=True, name_index="GRVI")
        df = pd.merge(df, idx, on='var', how='left')
        updateProgress(prog)
        # channels
        for i in range(self.imgs.depth):
            idx = self.getDfIndex(ch_1=i, isSingle=True,
                                  name_index="ch_%d" % i)
            df = pd.merge(df, idx, on='var', how='left')
            updateProgress(prog)

        # cluster
        idx = self.getDfCluster()
        df = pd.merge(df, idx, on='var', how='left')
        # export
        df.to_csv(os.path.join(path, prefix+"_data.csv"), index=False)

        # Figures
        pltImShow(self.imgs.get("crop"), path=path,
                  prefix=prefix, filename="_raw.png")
        updateProgress(prog)
        pltSegPlot(self.agents, self.imgs.get("crop")[:, :, :3],
                   isRect=True, path=path, prefix=prefix, filename="_rgb.png")
        updateProgress(prog)
        pltImShow(self.imgs.get("kmean"), path=path,
                  prefix=prefix, filename="_kmeans.png")
        updateProgress(prog)
        pltSegPlot(self.agents, self.imgs.get("visSeg"),
                   isRect=True, path=path, prefix=prefix, filename="_seg.png")
        updateProgress(prog)
        pltSegPlot(self.agents, self.imgs.get("bin"),
                isRect=True, path=path, prefix=prefix, filename="_bin.png")
        updateProgress(prog)

    def getDF(self):
        df = pd.DataFrame(columns=['var', 'row', 'col',\
                                'area_all', 'area_veg'])
        for row in range(self.agents.nRow):
            for col in range(self.agents.nCol):
                agent = self.agents.get(row, col)
                if agent.isFake():
                    continue
                entry = dict(var=agent.name, row=agent.row, col=agent.col)
                border_N = agent.getBorder(Dir.NORTH)
                border_W = agent.getBorder(Dir.WEST)
                border_S = agent.getBorder(Dir.SOUTH)
                border_E = agent.getBorder(Dir.EAST)
                rg_row = range(border_N, border_S)
                rg_col = range(border_W, border_E)
                img_bin_agent = self.imgs.get('bin')[rg_row, :][:, rg_col]
                entry['area_all'] = len(rg_row)*len(rg_col)
                entry['area_veg'] = img_bin_agent.sum()
                df.loc[len(df)] = entry
        return df

    def getDfIndex(self, ch_1, ch_2=-1, ch_3=-1, isSingle=False, isRatio=False, isContrast=False, isThree=False, name_index="index"):
        img_raw = self.imgs.get("crop").copy().astype(np.int)
        if img_raw.shape[2]==3 and ch_1==3:
            ch_1 = 1
        if isSingle:
            img_index = (img_raw[:,:,ch_1])
        if isRatio:
            img_index = img_raw[:,:,ch_1]/(img_raw[:,:,ch_2]+1e-8)
        if isContrast:
            img_index = (img_raw[:,:,ch_1]-img_raw[:,:,ch_2])/(img_raw[:,:,ch_1]+img_raw[:,:,ch_2]+1e-8)
        if isThree:
            img_index = (2*img_raw[:,:,ch_1]-img_raw[:,:,ch_2]-img_raw[:,:,ch_3])/(img_raw[:,:,ch_1]+img_raw[:,:,ch_2]+img_raw[:,:,ch_3]+1e-8)
        df = pd.DataFrame(columns=['var', 'index'])
        for row in range(self.agents.nRow):
            for col in range(self.agents.nCol):
                agent = self.agents.get(row, col)
                if not agent or agent.isFake():
                    continue
                entry = dict(var=agent.name, index=0)
                rg_row = range(agent.getBorder(Dir.NORTH), agent.getBorder(Dir.SOUTH))
                rg_col = range(agent.getBorder(Dir.WEST), agent.getBorder(Dir.EAST))
                img_bin_agent = self.imgs.get('bin')[rg_row, :][:, rg_col]
                img_index_agent = img_index[rg_row, :][:, rg_col]
                n_veg = img_bin_agent.sum()
                sum_index = np.multiply(img_bin_agent, img_index_agent).sum()
                entry['index'] = sum_index/(n_veg+1e-8)
                df.loc[len(df)] = entry
        df.columns = ['var', name_index]
        df = df[~df['var'].isnull()]
        return df

    def getDfCluster(self):
        # get var name
        df_final = pd.DataFrame(columns=['var'])
        for row in range(self.agents.nRow):
            for col in range(self.agents.nCol):
                agent = self.agents.get(row, col)
                entry = dict(var=agent.name)
                df_final.loc[len(df_final)] = entry
        # get cluster
        cluster = 0
        for i in self.imgs.paramKMs["lsSelect"]:
            img_index = ((np.isin(self.imgs.get("kmean"), i))*1).astype(np.int)
            df = pd.DataFrame(columns=['var', 'index'])
            for row in range(self.agents.nRow):
                for col in range(self.agents.nCol):
                    agent = self.agents.get(row, col)
                    if agent.isFake():
                        continue
                    entry = dict(var=agent.name, index=0)
                    rg_row = range(agent.getBorder(Dir.NORTH), agent.getBorder(Dir.SOUTH))
                    rg_col = range(agent.getBorder(Dir.WEST), agent.getBorder(Dir.EAST))
                    img_bin_agent = self.imgs.get("bin")[rg_row, :][:, rg_col]
                    img_index_agent = img_index[rg_row, :][:, rg_col]
                    n_veg = img_bin_agent.sum()
                    sum_index = np.multiply(img_bin_agent, img_index_agent).sum()
                    entry['index'] = sum_index/(n_veg+1e-8)
                    df.loc[len(df)] = entry
            df.columns = ['var', "cluster_%d"%cluster]
            df_final = pd.merge(df_final, df, on='var', how='left')
            cluster += 1

        df_final = df_final[~df_final['var'].isnull()]
        return df_final

