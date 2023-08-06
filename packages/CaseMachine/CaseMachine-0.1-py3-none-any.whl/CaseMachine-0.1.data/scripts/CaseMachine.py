#coding: UTF-8

# ===========================================================================
# CaseMachine (prototype for iteration 02 of inSitu)
# ---------------------------------------------------------------------------
# (c) 2015 Markus Hillebrand, Dipl.Inf.(FH) - www.markus-hillebrand.de
# Markus Hillebrand, Amalienstr. 71, 80799 München, Germany
# See LICENSE for more copyright details.
# ===========================================================================

import collections, datetime, weakref

class CaseMachineEvent:
    def __init__(self, nameValue, value):
        self.nameValue=nameValue
        self.value=value
        
    def cleanup(self):
        """Release unneeded references after processing handleValue(). To avoid 
           multiple evaluation of cases it's enough to have the id(event). 
           You can overwrite this method to keep all information about the last
           event/value if you want to.
        """
        del self.nameValue
        del self.value

class CaseMachine:            
    def __init__(self):
        self.mapValues={}
        self.mapCaseDependencies={}
        self.mapCases={}
        self.currentEvent=None
        
    def _createCaseMachineEvent(self, nameValue, value):
        return CaseMachineEvent(nameValue, value)
    
    def handleValue(self, nameValue, value):
        self.mapValues[nameValue]=value
        currentEvent=self._createCaseMachineEvent(nameValue, value)
        try:
            for case in self.mapCaseDependencies[nameValue]:
                case.handleEvent(currentEvent)
        except KeyError:
            pass
        finally:
            currentEvent.cleanup()
    
    def addCase(self, case):
        for dependency in case.dependencies:
            try:                
                self.mapCaseDependencies[dependency].append(case)
            except KeyError:
                self.mapCaseDependencies[dependency]=[case]
        return case
    