#Test file for functions in PipeFlowMain.py
#unit testing is very important to make sure minor increments work
#there is a python package unittest you can use or write your own unit test.
import PipeFlowMain as pf


#Each function in PipeFlowMain.py needs to be tested with known input and output.
#Here is how I write unittests. 
# test_functionname_testnumber = file.functionname(known inputs) == known output

test_getFrictionFactor_1 = pf.getFrictionFactor('Known Inputs') == 'Known Output' 

#Then its helpful to print a statement if it passes or if it fails the output
def test_results_print(result, func, output, inputs):
    """ Printer function for test results.
        results := Boolean 
        func    := Function Object
        output  := Function Output
        input   := (arg1, arg2, ... argN) tuple
    """
    if result is True:
        print('Test {} PASSED'.format(func.__name__))
    else:
        print('Test {} FAILED: Output:{} not {}'.format(func.__name__, output, func(*inputs)))

test_results_print(test_getFrictionFactor_1, pf.getFrictionFactor, 'True Answer', 'used inputs')


