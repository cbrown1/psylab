# -*- coding: utf-8 -*-

from gustav_forms import qt_Speech as theForm

ExpName = "An Experiment!"
ExpVars = "Conditions: 1,2,3\nData File: data.dat" 
BlockVars = "Target: Male\nMasker: Female\nSNR: +10"

token = "See Bill run."

block = 1
nblocks = 12
condition = 7

validKeys = '0,1,2,3,4,5,6,7,8,9'.split(',')
correctKey = '1'
quitKeys = '/,q'.split(',')

interface = theForm.Interface()

interface.updateInfo_Exp(ExpName)
interface.updateInfo_expVariables(ExpVars)
interface.updateInfo_BlockCount("Block %g of %g" % (block, nblocks))
interface.updateInfo_Block("Block %g of %g | Condition # %g" % (block, nblocks, condition))
interface.updateInfo_blockVariables(BlockVars)

interface.app.processEvents()
ret = interface.get_resp()
if str(ret) in validKeys:
    resp = ret
elif str(ret) in quitKeys:
    resp = "Cancelled by user"

print(resp)

