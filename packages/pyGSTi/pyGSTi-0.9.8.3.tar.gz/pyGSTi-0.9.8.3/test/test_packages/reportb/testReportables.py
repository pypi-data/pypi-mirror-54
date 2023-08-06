import unittest
import warnings
import collections
import pickle
import pygsti
import os
from pygsti.construction import std1Q_XYI as std
from ..testutils import BaseTestCase, compare_files, temp_files

import numpy as np

from pygsti.report import reportables as rptbl

class TestReportables(BaseTestCase):

    def setUp(self):
        super(TestReportables, self).setUp()

    def test_helpers(self):
        self.assertTrue(rptbl._nullFn("Any arguments") is None)

        self.assertAlmostEqual(rptbl._projectToValidProb(-0.1), 0.0)
        self.assertAlmostEqual(rptbl._projectToValidProb(1.1), 1.0)
        self.assertAlmostEqual(rptbl._projectToValidProb(0.5), 0.5)

        nan_qty = rptbl.evaluate(None) # none function -> nan qty
        self.assertTrue( np.isnan(nan_qty.value) )

        #deprecated:
        rptbl.decomposition( std.target_model().operations['Gx'] )
        rptbl.decomposition( np.zeros( (4,4), 'd') )        

    def test_functions(self):
        
        gs1 = std.target_model().depolarize(op_noise=0.1, spam_noise=0.05)
        gs2 = std.target_model()
        gl = "Gx" # operation label
        opstr = pygsti.obj.Circuit( ('Gx','Gx') )
        syntheticIdles = pygsti.construction.circuit_list( [
             ('Gx',)*4, ('Gy',)*4 ] )

        gatesetfn_factories = (  # model, oplabel
            rptbl.Choi_matrix,
            rptbl.Choi_evals,
            rptbl.Choi_trace,
            rptbl.Gate_eigenvalues, #GAP
            rptbl.Upper_bound_fidelity ,
            rptbl.Closest_ujmx, 
            rptbl.Maximum_fidelity,
            rptbl.Maximum_trace_dist, 

        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,gl)
            rptbl.evaluate(gsf)


        gatesetfn_factories = ( # model, circuit
            rptbl.Circuit_eigenvalues,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,opstr)
            rptbl.evaluate(gsf)


        gatesetfn_factories = ( # modelA, modelB, circuit
            rptbl.Rel_circuit_eigenvalues,
            rptbl.Circuit_fro_diff ,
            rptbl.Circuit_entanglement_infidelity,
            rptbl.Circuit_avg_gate_infidelity,
            rptbl.Circuit_jt_diff,
            rptbl.Circuit_half_diamond_norm,
            rptbl.Circuit_nonunitary_entanglement_infidelity,
            rptbl.Circuit_nonunitary_avg_gate_infidelity,
            rptbl.Circuit_eigenvalue_entanglement_infidelity,
            rptbl.Circuit_eigenvalue_avg_gate_infidelity,
            rptbl.Circuit_eigenvalue_nonunitary_entanglement_infidelity,
            rptbl.Circuit_eigenvalue_nonunitary_avg_gate_infidelity,
            rptbl.Circuit_eigenvalue_diamondnorm,
            rptbl.Circuit_eigenvalue_nonunitary_diamondnorm,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,gs2,opstr)
            rptbl.evaluate(gsf)


        gatesetfn_factories = ( # modelA, modelB, povmlbl
            rptbl.POVM_entanglement_infidelity,
            rptbl.POVM_jt_diff,
            rptbl.POVM_half_diamond_norm,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,gs2,"Mdefault")
            rptbl.evaluate(gsf)


        gatesetfn_factories = (  # model
            rptbl.Spam_dotprods,
            rptbl.Angles_btwn_rotn_axes,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1)
            rptbl.evaluate(gsf)


        gatesetfn_factories = ( # modelA, modelB, gatelbl
            rptbl.Entanglement_fidelity,
            rptbl.Entanglement_infidelity,
            rptbl.Closest_unitary_fidelity,
            rptbl.Fro_diff,
            rptbl.Jt_diff,
            rptbl.Half_diamond_norm,
            rptbl.Nonunitary_entanglement_infidelity,
            rptbl.Nonunitary_avg_gate_infidelity,
            rptbl.Eigenvalue_nonunitary_entanglement_infidelity, 
            rptbl.Eigenvalue_nonunitary_avg_gate_infidelity, 
            rptbl.Eigenvalue_entanglement_infidelity, 
            rptbl.Eigenvalue_avg_gate_infidelity, 
            rptbl.Eigenvalue_diamondnorm, 
            rptbl.Eigenvalue_nonunitary_diamondnorm, 
            rptbl.Avg_gate_infidelity, 
            rptbl.Model_model_angles_btwn_axes, 
            rptbl.Rel_eigvals, 
            rptbl.Rel_logTiG_eigvals, 
            rptbl.Rel_logGTi_eigvals, 
            rptbl.Rel_logGmlogT_eigvals, 
            rptbl.Rel_gate_eigenvalues, 
            rptbl.LogTiG_and_projections, 
            rptbl.LogGTi_and_projections, 
            rptbl.LogGmlogT_and_projections, 
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,gs2,gl)
            rptbl.evaluate(gsf)


        gatesetfn_factories = ( # modelA, modelB, syntheticIdleStrs
            rptbl.Robust_LogGTi_and_projections,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,gs2, syntheticIdles )
            rptbl.evaluate(gsf)
            

        gatesetfn_factories = ( # modelA, modelB
            rptbl.General_decomposition,
            rptbl.Average_gateset_infidelity,
            rptbl.Predicted_rb_number,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,gs2)
            rptbl.evaluate(gsf)


        gatesetfn_factories = ( # model1, model2, label, typ
            rptbl.Vec_fidelity,
            rptbl.Vec_infidelity,
            rptbl.Vec_tr_diff,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,gs2,"rho0","prep")
            rptbl.evaluate(gsf)
            gsf = gsf_factory(gs1,gs2,"Mdefault:0","effect")
            rptbl.evaluate(gsf)


        gatesetfn_factories = ( # model, label, typ
            rptbl.Vec_as_stdmx,
            rptbl.Vec_as_stdmx_eigenvalues,
        )
        for gsf_factory in gatesetfn_factories:
            gsf = gsf_factory(gs1,"rho0","prep")
            rptbl.evaluate(gsf)
            gsf = gsf_factory(gs1,"Mdefault:0","effect")
            rptbl.evaluate(gsf)

    def test_nearby_gatesetfns(self):
        gs1 = std.target_model().depolarize(op_noise=0.1, spam_noise=0.05)
        gs2 = std.target_model()
        opstr = pygsti.obj.Circuit( ('Gx','Gx') )
        
        fn = rptbl.Half_diamond_norm(gs1,gs2,'Gx')
        if fn is not None:
            fn.evaluate(gs1)
            fn.evaluate_nearby(gs1)
        else:
            warnings.warn("Can't test Half_diamond_norm! (probably b/c cvxpy isn't available)")
        
        fn = rptbl.Circuit_half_diamond_norm(gs1,gs2,opstr)
        if fn is not None:
            fn.evaluate(gs1)
            fn.evaluate_nearby(gs1)
        else:
            warnings.warn("Can't test Circuit_half_diamond_norm! (probably b/c cvxpy isn't available)")

    def test_closest_unitary(self):
        gs1 = std.target_model().depolarize(op_noise=0.1, spam_noise=0.05)
        gs2 = std.target_model()
        rptbl.closest_unitary_fidelity(gs1.operations['Gx'], gs2.operations['Gx'], "pp") # op2 is unitary
        rptbl.closest_unitary_fidelity(gs2.operations['Gx'], gs1.operations['Gx'], "pp") # op1 is unitary

    def test_general_decomp(self):
        gs1 = std.target_model().depolarize(op_noise=0.1, spam_noise=0.05)
        gs2 = std.target_model()
        gs1.operations['Gx'] = np.array( [[-1, 0, 0, 0],
                                     [ 0,-1, 0, 0],
                                     [ 0, 0, 1, 0],
                                     [ 0, 0, 0, 1]], 'd') # -1 eigenvalues => use approx log.
        rptbl.general_decomposition(gs1,gs2)
        



#Test functions within reportables separately? This version of the test is outdated:
#    def test_reportables(self):
#        #Test that None is returned when qty cannot be computed
#        qty = pygsti.report.reportables.compute_dataset_qty("FooBar",self.ds)
#        self.assertIsNone(qty)
#        qty = pygsti.report.reportables.compute_gateset_qty("FooBar",self.mdl_clgst)
#        self.assertIsNone(qty)
#        qty = pygsti.report.reportables.compute_gateset_dataset_qty("FooBar",self.mdl_clgst, self.ds)
#        self.assertIsNone(qty)
#        qty = pygsti.report.reportables.compute_gateset_gateset_qty("FooBar",self.mdl_clgst, self.mdl_clgst)
#        self.assertIsNone(qty)
#
#        #test ignoring operation sequences not in dataset
#        qty = pygsti.report.reportables.compute_dataset_qty("operation sequence length", self.ds,
#                                                            pygsti.construction.circuit_list([('Gx','Gx'),('Gfoobar',)]) )
#        qty = pygsti.report.reportables.compute_gateset_dataset_qty("prob(0) diff", self.mdl_clgst, self.ds,
#                                                            pygsti.construction.circuit_list([('Gx','Gx'),('Gfoobar',)]) )
#        qty_str = str(qty) #test __str__
#
#        #Test model gates mismatch
#        from pygsti.construction import std1Q_XY as stdXY
#        with self.assertRaises(ValueError):
#            qty = pygsti.report.reportables.compute_gateset_gateset_qty(
#                "Gx fidelity",std.target_model(), stdXY.target_model()) #Gi missing from 2nd model
#        with self.assertRaises(ValueError):
#            qty = pygsti.report.reportables.compute_gateset_gateset_qty(
#                "Gx fidelity",stdXY.target_model(), std.target_model()) #Gi missing from 1st model



#def test_results_object(self):
#    results = pygsti.report.Results()
#    results.init_single("logl", self.targetModel, self.ds, self.mdl_clgst,
#                        self.lgstStrings, self.targetModel)
#
#    results.parameters.update(
#        {'minProbClip': 1e-6, 'minProbClipForWeighting': 1e-4,
#         'probClipInterval': (-1e6,1e6), 'radius': 1e-4,
#         'weights': None, 'defaultDirectory': temp_files + "",
#         'defaultBasename': "MyDefaultReportName",
#         'hessianProjection': 'std'} )
#
#    results.create_full_report_pdf(
#        filename=temp_files + "/singleReport.pdf")
#    results.create_brief_report_pdf(
#        filename=temp_files + "/singleBrief.pdf")
#    results.create_presentation_pdf(
#        filename=temp_files + "/singleSlides.pdf")
#    if self.have_python_pptx:
#        results.create_presentation_ppt(
#            filename=temp_files + "/singleSlides.ppt", pptTables=True)
#
#    #test tree splitting of hessian
#    results.parameters['memLimit'] = 10*(1024)**2 #10MB
#    results.create_brief_report_pdf(confidenceLevel=95,
#        filename=temp_files + "/singleBriefMemLimit.pdf")
#    results.parameters['memLimit'] = 10 #10 bytes => too small
#    with self.assertRaises(MemoryError):
#        results.create_brief_report_pdf(confidenceLevel=90,
#           filename=temp_files + "/singleBriefMemLimit.pdf")
#
#
#    #similar test for chi2 hessian
#    results2 = pygsti.report.Results()
#    results2.init_single("chi2", self.targetModel, self.ds, self.mdl_clgst,
#                        self.lgstStrings, self.targetModel)
#    results2.parameters.update(
#        {'minProbClip': 1e-6, 'minProbClipForWeighting': 1e-4,
#         'probClipInterval': (-1e6,1e6), 'radius': 1e-4,
#         'weights': None, 'defaultDirectory': temp_files + "",
#         'defaultBasename': "MyDefaultReportName",
#         'hessianProjection': "std"} )
#    results2.parameters['memLimit'] = 10*(1024)**2 #10MB
#    results2.create_brief_report_pdf(confidenceLevel=95,
#        filename=temp_files + "/singleBriefMemLimit2.pdf")
#    results2.parameters['memLimit'] = 10 #10 bytes => too small
#    with self.assertRaises(MemoryError):
#        results2.create_brief_report_pdf(confidenceLevel=90,
#           filename=temp_files + "/singleBriefMemLimit2.pdf")
#
#
#
#
#    results_str = str(results)
#    tableNames = list(results.tables.keys())
#    figNames = list(results.figures.keys())
#    for g in results.models:
#        s = str(g)
#    for g in results.circuit_lists:
#        s = str(g)
#    s = str(results.dataset)
#    s = str(results.options)
#
#    self.assertTrue(tableNames[0] in results.tables)
#
#    with self.assertRaises(KeyError):
#        x = results.tables.get('foobar')
#    with self.assertRaises(ValueError):
#        results.tables['newKey'] = "notAllowed"
#    with self.assertRaises(NotImplementedError):
#        for x in results.tables: # cannot __iter__
#            print(x)
#    with self.assertRaises(NotImplementedError):
#        for x in results.tables.iteritems(): # cannot iter
#            print(x)
#    with self.assertRaises(NotImplementedError):
#        for x in list(results.tables.values()): # cannot iter
#            print(x)
#
#    pkl = pickle.dumps(results)
#    results_copy = pickle.loads(pkl)
#    self.assertEqual(tableNames, list(results_copy.tables.keys()))
#    self.assertEqual(figNames, list(results_copy.figures.keys()))
#    #self.assertEqual(results.options, results_copy.options) #need to add equal test to ResultsOptions
#    self.assertEqual(results.parameters, results_copy.parameters)
#
#    results2 = pygsti.report.Results()
#    results2.options.template_path = "/some/path/to/templates"
#    results2.options.latex_cmd = "myCustomLatex"
#
#    #bad objective function name
#    results_badObjective = pygsti.report.Results()
#    #results_badObjective.init_single("foobar", self.targetModel, self.ds, self.mdl_clgst,
#    #                                 self.lgstStrings)
#    results_badObjective.init_Ls_and_germs("foobar", self.targetModel, self.ds, self.mdl_clgst, [0], self.germs,
#                                           [self.mdl_clgst], [self.lgstStrings], self.fiducials, self.fiducials,
#                                           pygsti.construction.repeat_with_max_length, True)
#
#    with self.assertRaises(ValueError):
#        results_badObjective._get_confidence_region(95)
#    with self.assertRaises(ValueError):
#        results_badObjective._specials['DirectLongSeqGatesets']
#    with self.assertRaises(ValueError):
#        results_badObjective.create_full_report_pdf(filename=temp_files + "/badReport.pdf")
#    with self.assertRaises(ValueError):
#        results_badObjective.create_presentation_pdf(filename=temp_files + "/badSlides.pdf")
#    if self.have_python_pptx:
#        with self.assertRaises(ValueError):
#            results_badObjective.create_presentation_ppt(filename=temp_files + "/badSlides.pptx")


if __name__ == "__main__":
    unittest.main(verbosity=2)
