import b3

'''
Created on 27 de set. 2017

@author: dagush
'''

__all__ = ['IfThenElse']

class IfThenElse(b3.Condition):
    def __init__(self, queryChild=None, thenChild=None, elseChild=None):
        super(IfThenElse, self).__init__()
        self.queryChild = queryChild
        self.thenChild = thenChild
        self.elseChild = elseChild
    def tick(self, tick):
        if not self.queryChild and not self.thenChild:
            return b3.ERROR
        
        status = self.queryChild._execute(tick)
        finalStatus = status
        
        if status == b3.SUCCESS:
            finalStatus = self.thenChild._execute(tick)
        elif status == b3.FAILURE:
            if self.elseChild:
                finalStatus = self.elseChild._execute(tick)
        
        return finalStatus
        
