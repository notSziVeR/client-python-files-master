import ui
import app
import exception
from _weakref import proxy

class GlobalRankingButton(ui.Button):

    BUTTON_N = "d:/ymir work/ui/game/battle_pass/battle_pass_normal.png"
    BUTTON_H = "d:/ymir work/ui/game/battle_pass/battle_pass_over.png"
    BUTTON_D = "d:/ymir work/ui/game/battle_pass/battle_pass_down.png"

    def __init__(self):
        ui.Button.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        ui.Button.__del__(self)

    def Destroy(self):
        pass

    def __LoadWindow(self):
        ## Build button
        self.SetUpVisual(self.BUTTON_N)
        self.SetOverVisual(self.BUTTON_H)
        self.SetDownVisual(self.BUTTON_D)

        ## Bind tooltip
        self.SetToolTipText("Global ranking")

        ## Position it
        self.Show()

class GlobalRanking(ui.ScriptWindow):

    CATEGORY_MAX_NUM = 6
    RANKING_MAX_NUM = 10
    RANKING_SELF_KEY = RANKING_MAX_NUM
    RANKING_FIELD_GAP = 26

    class RankingCategoryButton(ui.Button):

        IMAGE_PATTERN = "global_ranking/btn_{}_{}.png"
        WINDOW_SIZE = (143, 42)

        def __init__(self, rParent, rEvent, iNum):
            ui.Button.__init__(self)
            self.rParent = proxy(rParent)
            self.iNum = iNum
            self.rEvent = rEvent
            self.__BuildWindow()

        def __del__(self):
            ui.Button.__del__(self)

        def __eq__(self, rOther):
            if isinstance(rOther, GlobalRanking.RankingCategoryButton):
                return self.iNum == rOther.iNum

            raise NotImplemented

        def __ne__(self, rOther):
            return not self.__eq__(rOther)

        def __BuildWindow(self):
            ## Size
            self.SetSize(*self.WINDOW_SIZE)

            ## Design
            self.SetUpVisual(self.IMAGE_PATTERN.format(self.iNum, 0))
            self.SetOverVisual(self.IMAGE_PATTERN.format(self.iNum, 1))
            self.SetDownVisual(self.IMAGE_PATTERN.format(self.iNum, 1))

            ## Event
            self.SetEvent(self.__ClickButton)

        def __ClickButton(self):
            ## Release hover over any other buttons
            for rBut in self.rParent.itemList:
                if rBut != self:
                    rBut.SetUpVisual(self.IMAGE_PATTERN.format(rBut.iNum, 0))
                else:
                    rBut.SetUpVisual(self.IMAGE_PATTERN.format(rBut.iNum, 1))

            ## Now fire saved event
            self.rEvent()

    class RankingWindow(ui.Window):

        WINDOW_SIZE = (348, 21)
        FIELD_SIZE = {"Pos" : (31, 21), "Name" : (106, 21), "Empire" : (106, 21), "Score" : (102, 21)}
        FIELD_POS = {"Pos" : (0, 0), "Name" : (32, 0), "Empire" : (139, 0), "Score" : (246, 0)}
        EMPIRE_NAMES = {1 : "Shinsoo", 2 : "Chunjo", 3 : "Jinno"}

        def __init__(self):
            ui.Window.__init__(self)
            self.Objects = {}
            self.__BuildWindow()

        def __del__(self):
            ui.Window.__del__(self)
            self.Objects = {}

        def __BuildWindow(self):
            ## Size
            self.SetSize(*self.WINDOW_SIZE)

            ## Generate fields
            for sKey in self.FIELD_SIZE.keys():
                sKeyName = "{}_Field".format(sKey)
                self.Objects[sKeyName] = ui.Window()
                self.Objects[sKeyName].SetParent(self)
                self.Objects[sKeyName].SetSize(*self.FIELD_SIZE[sKey])
                self.Objects[sKeyName].SetPosition(*self.FIELD_POS[sKey])
                self.Objects[sKeyName].Show()

                ## Generate corresponding text lines
                self.Objects["{}_Text".format(sKey)] = ui.MakeTextLine(self.Objects[sKeyName])

        def SetData(self, sName, iEmpire, iScore, iPos = -1):
            if iEmpire == -1:
                ## Set it blank
                self.Objects["Name_Text"].SetText("")
                self.Objects["Empire_Text"].SetText("")
                self.Objects["Score_Text"].SetText("")
            else:
                self.Objects["Name_Text"].SetText(sName)
                self.Objects["Empire_Text"].SetText(self.EMPIRE_NAMES.get(iEmpire, "Unknown"))
                if type(iScore) is not float:
                    self.Objects["Score_Text"].SetText('.'.join([ i-3<0 and str(iScore)[:i] or str(iScore)[i-3:i] for i in range(len(str(iScore))%3, len(str(iScore))+1, 3) if i ]))
                else:
                    self.Objects["Score_Text"].SetText(iScore)

            if iPos > -1:
                self.Objects["Pos_Text"].SetText(str(iPos))
            else:
                self.Objects["Pos_Text"].SetText("")

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.Objects = {}
        self.iCurCat = -1
        self.RANKING_DATA = dict()
        self.__LoadWindow()

    def __del__(self):
        self.Objects = {}
        self.iCurCat = -1
        self.RANKING_DATA = dict()

    def Destroy(self):
        self.ClearDictionary()
        self.Objects = {}
        self.iCurCat = -1
        self.RANKING_DATA = dict()

    def    __LoadWindow(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "uiscript/global_ranking.py")
        except:
            exception.exception("GlobalRanking.__LoadWindow.LoadObject")

        try:
            self.Objects["Board"] = self.GetChild("EventBoard")

            ## Categories
            self.Objects["RankingCategories"] = self.GetChild("RankingCategories")
            self.Objects["RankingCategoriesScrollBar"] = self.GetChild("ScrollBar")

            ## Records
            self.Objects["RankingRecords"] = self.GetChild("RankingRecords")

        except:
            exception.exception("GlobalRanking.__LoadWindow.BindObject")

        self.Objects["Board"].SetCloseEvent(self.Hide)

        ## Setup categories
        self.Objects["RankingCategories"].SetScrollBar(self.Objects["RankingCategoriesScrollBar"])
        self.Objects["RankingCategories"].SetItemSize(*self.RankingCategoryButton.WINDOW_SIZE)
        self.Objects["RankingCategories"].SetItemStep(self.RankingCategoryButton.WINDOW_SIZE[1] + 5)

        ## Fill categories
        for iNum in xrange(self.CATEGORY_MAX_NUM):
            categoryBut = self.RankingCategoryButton(self.Objects["RankingCategories"], lambda me = proxy(self), iNum_ = iNum: me.SwitchCategory(iNum_), iNum)
            self.Objects["RankingCategories"].AppendItem(categoryBut)
            self.RANKING_DATA[iNum] = {i : ("", -1, -1, -1) for i in xrange(self.RANKING_MAX_NUM + 1)}

        ## Fill rankings (blank fields)
        self.Objects["RankingObjects"] = {}
        for iNum in xrange(self.RANKING_MAX_NUM + 1): ## Include "self" position
            rankWindow = self.RankingWindow()
            rankWindow.SetParent(self.Objects["RankingRecords"])
            rankWindow.SetPosition(1, 1 + (iNum * self.RANKING_FIELD_GAP))
            rankWindow.Show()
            self.Objects["RankingObjects"][iNum] = rankWindow

        self.SetCenterPosition()
        self.SetTop()
        self.Hide()

    def UpdateRankingData(self, iCategory, iNum, sName, iEmpire, lScore):
        print "Incoming data", iCategory, iNum, sName, iEmpire, lScore
        self.RANKING_DATA[iCategory][iNum] = (sName, iEmpire, lScore, -1)

    def UpdateRankingData_Self(self, iCategory, iPos, sName, iEmpire, lScore):
        print "Incoming self data", iCategory, iPos, sName, iEmpire, lScore
        self.RANKING_DATA[iCategory][self.RANKING_SELF_KEY] = (sName, iEmpire, lScore, iPos)

    def SwitchCategory(self, iNum):
        ## RadioButtons were already update so simply process raw logic
        self.iCurCat = iNum
        self.__Refresh()

    def __Refresh(self):
        if self.iCurCat == -1:
            return

        ## Update TOP records
        for i in xrange(self.RANKING_MAX_NUM):
            self.Objects["RankingObjects"][i].SetData(*self.RANKING_DATA[self.iCurCat][i])

        ## Update "self" record
        self.Objects["RankingObjects"][self.RANKING_SELF_KEY].SetData(*self.RANKING_DATA[self.iCurCat][self.RANKING_SELF_KEY])

    def Simulate(self):
        for i in xrange(self.CATEGORY_MAX_NUM):
            for x in xrange(self.RANKING_MAX_NUM):
                self.UpdateRankingData(i, x, "{}".format(app.GetRandom(1, 100000)), -1, app.GetRandom(10, 10000))
    
            self.UpdateRankingData_Self(i, app.GetRandom(10, 1000), "{}".format(app.GetRandom(1, 100000)), -1, app.GetRandom(10, 10000))

        self.__Refresh()

    def UpdateWindow(self):
        if self.IsShow():
            self.Hide()
        else:
            self.Show()
            self.__Refresh()

