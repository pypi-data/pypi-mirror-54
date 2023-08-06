import unittest
import pygsti
from pygsti.construction import std1Q_XYI as std
from pygsti.construction import std2Q_XYICNOT as std2Q
from pygsti.objects.mapforwardsim import MapForwardSimulator
import sys, os

from ..testutils import BaseTestCase, compare_files, temp_files

class DriversTestCase(BaseTestCase):

    def setUp(self):
        super(DriversTestCase, self).setUp()

        self.model = std.target_model()

        self.germs = std.germs
        self.fiducials = std.fiducials
        self.maxLens = [1,2,4]
        self.opLabels = list(self.model.operations.keys())

        self.elgstStrings = pygsti.construction.make_elgst_lists(
            self.opLabels, self.germs, self.maxLens )

        self.lsgstStrings = pygsti.construction.make_lsgst_lists(
            self.opLabels, self.fiducials, self.fiducials, self.germs, self.maxLens )

        self.lsgstStrings_tgp = pygsti.construction.make_lsgst_lists(
            self.opLabels, self.fiducials, self.fiducials, self.germs, self.maxLens,
            truncScheme="truncated germ powers" )

        self.lsgstStrings_lae = pygsti.construction.make_lsgst_lists(
            self.opLabels, self.fiducials, self.fiducials, self.germs, self.maxLens,
            truncScheme='length as exponent' )

        ## RUN BELOW LINES TO GENERATE SAVED DATASETS
        if os.environ.get('PYGSTI_REGEN_REF_FILES','no').lower() in ("yes","1","true","v2"): # "v2" to only gen version-dep files
            datagen_gateset = self.model.depolarize(op_noise=0.05, spam_noise=0.1)
            datagen_gateset2 = self.model.depolarize(op_noise=0.1, spam_noise=0.03).rotate((0.05,0.13,0.02))
            ds = pygsti.construction.generate_fake_data(
                datagen_gateset, self.lsgstStrings[-1],
                nSamples=1000,sampleError='binomial', seed=100)
            ds2 = pygsti.construction.generate_fake_data(
                datagen_gateset2, self.lsgstStrings[-1],
                nSamples=1000,sampleError='binomial', seed=100)
            ds2 = ds2.copy_nonstatic()
            ds2.add_counts_from_dataset(ds)
            ds2.done_adding_data()
            ds_tgp = pygsti.construction.generate_fake_data(
                datagen_gateset, self.lsgstStrings_tgp[-1],
                nSamples=1000,sampleError='binomial', seed=100)
        
            ds_lae = pygsti.construction.generate_fake_data(
                datagen_gateset, self.lsgstStrings_lae[-1],
                nSamples=1000,sampleError='binomial', seed=100)
            ds.save(compare_files + "/drivers.dataset%s" % self.versionsuffix)
            ds2.save(compare_files + "/drivers2.dataset%s" % self.versionsuffix) #non-markovian
            ds_tgp.save(compare_files + "/drivers_tgp.dataset%s" % self.versionsuffix)
            ds_lae.save(compare_files + "/drivers_lae.dataset%s" % self.versionsuffix)

class TestDriversMethods(DriversTestCase):

    def test_longSequenceGST_WholeGermPowers(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        ts = "whole germ powers"

        maxLens = self.maxLens
        result = pygsti.do_long_sequence_gst( #self.runSilent(
                                ds, std.target_model(), std.fiducials, std.fiducials,
                                std.germs, maxLens, advancedOptions={'truncScheme': ts})

        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, std.target_model(), std.fiducials, std.fiducials,
                                std.germs, maxLens,
                                advancedOptions={'truncScheme': ts, 'objective': "chi2"})


        #Try using files instead of objects
        pygsti.io.write_model(std.target_model(), temp_files + "/driver.model")
        pygsti.io.write_dataset(temp_files + "/driver_test_dataset.txt",
                                ds, self.lsgstStrings[-1])
        pygsti.io.write_circuit_list(temp_files + "/driver_fiducials.txt", std.fiducials)
        pygsti.io.write_circuit_list(temp_files + "/driver_germs.txt", std.germs)

        result = self.runSilent(pygsti.do_long_sequence_gst,
                                temp_files + "/driver_test_dataset.txt",
                                temp_files + "/driver.model",
                                temp_files + "/driver_fiducials.txt",
                                temp_files + "/driver_fiducials.txt",
                                temp_files + "/driver_germs.txt",
                                maxLens, advancedOptions={'truncScheme': ts,
                                                          'randomizeStart': 1e-6,
                                                          'profile': 2,
                                                          'verbosity': 10,
                                                          'memoryLimitInBytes': 2*1000**3})
                        # Also try profile=2 and deprecated advanced options here (above)

        #check invalid profile options
        with self.assertRaises(ValueError):
            pygsti.do_long_sequence_gst(ds, std.target_model(), std.fiducials, std.fiducials,
                                        std.germs, maxLens,
                                        advancedOptions={'profile': 3})

        #Try using effectStrs == None and some advanced options
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, std.target_model(), std.fiducials, None,
                                std.germs, maxLens,
                                advancedOptions={'starting point': std.target_model(),
                                                 'depolarizeStart': 0.05,
                                                 'truncScheme': ts,
                                                 'cptpPenaltyFactor': 1.0})
                                            # OLD: 'contractStartToCPTP': True,


        #Check errors
        with self.assertRaises(ValueError):
            self.runSilent(pygsti.do_long_sequence_gst,
                           ds, std.target_model(), std.fiducials, None,
                           std.germs, maxLens,
                           advancedOptions={'truncScheme': ts, 'objective': "FooBar"}) #bad objective
        with self.assertRaises(ValueError):
            self.runSilent(pygsti.do_long_sequence_gst,
                           ds, std.target_model(), std.fiducials, None,
                           std.germs, maxLens,
                           advancedOptions={'truncScheme': ts, 'starting point': "FooBar"}) #bad objective



    def test_longSequenceGST_TruncGermPowers(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers_tgp.dataset%s" % self.versionsuffix)
        ts = "truncated germ powers"

        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
            ds, std.target_model(), std.fiducials, std.fiducials,
            std.germs, maxLens, advancedOptions={'truncScheme': ts})

        result = self.runSilent(pygsti.do_long_sequence_gst,
            ds, std.target_model(), std.fiducials, std.fiducials,
            std.germs, maxLens,
            advancedOptions={'truncScheme': ts, 'objective': "chi2"})

        #result = self.runSilent(pygsti.do_long_sequence_gst,
        #    ds, std.target_model(), std.fiducials, std.fiducials,
        #    std.germs, maxLens, truncScheme=ts, constrainToTP=False)

    def test_longSequenceGST_LengthAsExponent(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers_lae.dataset%s" % self.versionsuffix)
        ts = "length as exponent"

        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
            ds, std.target_model(), std.fiducials, std.fiducials,
            std.germs, maxLens, advancedOptions={'truncScheme': ts})

        result = self.runSilent(pygsti.do_long_sequence_gst,
            ds, std.target_model(), std.fiducials, std.fiducials,
            std.germs, maxLens,
            advancedOptions={'truncScheme': ts, 'objective': "chi2"})

        #result = self.runSilent(pygsti.do_long_sequence_gst,
        #    ds, std.target_model(), std.fiducials, std.fiducials,
        #    std.germs, maxLens, truncScheme=ts, constrainToTP=False)



    def test_longSequenceGST_fiducialPairReduction(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        maxLens = self.maxLens

        #Make list-of-lists of GST operation sequences
        fullStructs = pygsti.construction.make_lsgst_structs(
            std.target_model(), std.fiducials, std.fiducials, std.germs, maxLens)

        lens = [ len(strct.allstrs) for strct in fullStructs ]
        self.assertEqual(lens, [92,168,450]) # ,817,1201, 1585]


        #Global FPR
        fidPairs = pygsti.alg.find_sufficient_fiducial_pairs(
            std.target_model(), std.fiducials, std.fiducials, std.germs,
            searchMode="random", nRandom=100, seed=1234,
            verbosity=1, memLimit=int(2*(1024)**3), minimumPairs=2)

        gfprStructs = pygsti.construction.make_lsgst_structs(
            std.target_model(), std.fiducials, std.fiducials, std.germs, maxLens,
            fidPairs=fidPairs)

        lens = [ len(strct.allstrs) for strct in gfprStructs ]
        #self.assertEqual(lens, [92,100,130]) #,163,196,229]
          #can't test reliably b/c "random" above
          # means different answers on different systems

        gfprExperiments = pygsti.construction.make_lsgst_experiment_list(
            std.target_model(), std.fiducials, std.fiducials, std.germs, maxLens,
            fidPairs=fidPairs)

        result = pygsti.do_long_sequence_gst_base(ds, std.target_model(), gfprStructs, verbosity=0)
        pygsti.report.create_standard_report(result, temp_files + "/full_report_GFPR",
                                             "GFPR report", verbosity=2)


        #Per-germ FPR
        fidPairsDict = pygsti.alg.find_sufficient_fiducial_pairs_per_germ(
            std.target_model(), std.fiducials, std.fiducials, std.germs,
            searchMode="random", constrainToTP=True,
            nRandom=100, seed=1234, verbosity=1,
            memLimit=int(2*(1024)**3))

        pfprStructs = pygsti.construction.make_lsgst_structs(
            std.target_model(), std.fiducials, std.fiducials, std.germs, maxLens,
            fidPairs=fidPairsDict) #note: fidPairs arg can be a dict too!

        lens = [ len(strct.allstrs) for strct in pfprStructs ]
        #self.assertEqual(lens, [92,99,138]) # ,185,233,281]
          #can't test reliably b/c "random" above
          # means different answers on different systems


        pfprExperiments = pygsti.construction.make_lsgst_experiment_list(
            std.target_model(), std.fiducials, std.fiducials, std.germs, maxLens,
            fidPairs=fidPairsDict)

        result = pygsti.do_long_sequence_gst_base(ds, std.target_model(), pfprStructs, verbosity=0)
        pygsti.report.create_standard_report(result, temp_files + "/full_report_PFPR",
                                             "PFPR report", verbosity=2)



    def test_longSequenceGST_randomReduction(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        ts = "whole germ powers"
        maxLens = self.maxLens

        #Without fixed initial fiducial pairs
        fidPairs = None
        reducedLists = pygsti.construction.make_lsgst_structs(
            std.target_model().operations.keys(), std.fiducials, std.fiducials, std.germs,
            maxLens, fidPairs, ts, keepFraction=0.5, keepSeed=1234)
        result = self.runSilent(pygsti.do_long_sequence_gst_base,
            ds, std.target_model(), reducedLists,
            advancedOptions={'truncScheme': ts})

        #create a report...
        pygsti.report.create_standard_report(result, temp_files + "/full_report_RFPR",
                                             "RFPR report", verbosity=2)

        #With fixed initial fiducial pairs
        fidPairs = pygsti.alg.find_sufficient_fiducial_pairs(
            std.target_model(), std.fiducials, std.fiducials, std.germs, verbosity=0)
        reducedLists = pygsti.construction.make_lsgst_structs(
            std.target_model().operations.keys(), std.fiducials, std.fiducials, std.germs,
            maxLens, fidPairs, ts, keepFraction=0.5, keepSeed=1234)
        result2 = self.runSilent(pygsti.do_long_sequence_gst_base,
                                 ds, std.target_model(), reducedLists,
                                 advancedOptions={'truncScheme': ts})

        #create a report...
        pygsti.report.create_standard_report(result2, temp_files + "/full_report_RFPR2.html",
                                             verbosity=2)


    #We're removing linear gates - at least building them
    #def test_longSequenceGST_linearGates(self):
    #    ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
    #    ts = "whole germ powers"
    #
    #    target_model = pygsti.construction.build_explicit_model([('Q0',)], ['Gi','Gx','Gy'],
    #                                                  [ "D(Q0)","X(pi/2,Q0)", "Y(pi/2,Q0)"],
    #                                                  parameterization="linear")
    #
    #    maxLens = self.maxLens
    #    result = self.runSilent(pygsti.do_long_sequence_gst,
    #                            ds, target_model, std.fiducials, std.fiducials,
    #                            std.germs, maxLens,
    #                            advancedOptions={'truncScheme': ts, 'tolerance':1e-4} )
    #                            #decrease tolerance
    #                            # b/c this problem seems hard to converge at the very end
    #                            # very small changes (~0.0001) to the total chi^2.
    #
    #    #create a report...
    #    pygsti.report.create_standard_report(result, temp_files + "/full_report_LPGates",
    #                                         "LPGates report", verbosity=2)


    def test_longSequenceGST_CPTP(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)

        target_model = std.target_model()
        target_model.set_all_parameterizations("CPTP")

        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, target_model, std.fiducials, std.fiducials,
                                std.germs, maxLens)

        #create a report...
        pygsti.report.create_standard_report(result, temp_files + "/full_report_CPTPGates",
                                             "CPTP Gates report", verbosity=2)


    def test_longSequenceGST_Sonly(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)

        target_model = std.target_model()
        target_model.set_all_parameterizations("S")

        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, target_model, std.fiducials, std.fiducials,
                                std.germs, maxLens)

        #create a report...
        pygsti.report.create_standard_report(result, temp_files + "/full_report_SGates.html",
                                             "SGates report", verbosity=2)


    def test_longSequenceGST_GLND(self):
        #General Lindbladian parameterization (allowed to be non-CPTP)
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)

        target_model = std.target_model()

        #No set_all_parameterizations option for this one, since it probably isn't so useful
        for lbl,gate in target_model.operations.items():
            target_model.operations[lbl] = pygsti.objects.operation.convert(gate, "GLND", "gm")
        target_model.default_gauge_group = pygsti.objects.UnitaryGaugeGroup(target_model.dim,"gm")
          #Lindblad gates only know how to do unitary transforms currently, even though
          # in the non-cptp case it they should be able to transform generally.

        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, target_model, std.fiducials, std.fiducials,
                                std.germs, maxLens)

        #create a report...
        pygsti.report.create_standard_report(result, temp_files + "/full_report_SGates",
                                             "SGates report", verbosity=2)


    def test_longSequenceGST_HplusS(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)

        target_model = std.target_model()
        target_model.set_all_parameterizations("H+S")

        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, target_model, std.fiducials, std.fiducials,
                                std.germs, maxLens)

        #create a report...
        pygsti.report.create_standard_report(result, temp_files + "/full_report_HplusSGates",
                                             "HpS report", verbosity=2)



    def test_longSequenceGST_wMapCalc(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        ts = "whole germ powers"

        target_model = std.target_model()
        target_model._calcClass = MapForwardSimulator

        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, target_model, std.fiducials, std.fiducials,
                                std.germs, maxLens, advancedOptions={'truncScheme': ts})


    def test_longSequenceGST_badfit(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        ts = "whole germ powers"

        #lower bad-fit threshold to zero to trigger bad-fit additional processing
        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, std.target_model(), std.fiducials, std.fiducials,
                                std.germs, maxLens, advancedOptions={'truncScheme': ts,
                                                                     'badFitThreshold': -100})

        pygsti.report.create_standard_report(result, temp_files + "/full_report_badfit",
                                             "badfit report", verbosity=2)

        result_chi2 = self.runSilent(pygsti.do_long_sequence_gst,
                                     ds, std.target_model(), std.fiducials, std.fiducials,
                                     std.germs, maxLens, advancedOptions={'truncScheme': ts,
                                                                          'badFitThreshold': -100,
                                                                          'objective': 'chi2'})

    def test_model_test(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        mdl_guess = std.target_model().depolarize(op_noise=0.01,spam_noise=0.01)

        maxLens = self.maxLens
        output_pkl_stream = open(temp_files + "/driverModelTestResult1.pkl",'wb')
        result = self.runSilent(pygsti.do_model_test, mdl_guess,
                                ds, std.target_model(), std.fiducials, std.fiducials,
                                std.germs, maxLens, output_pkl=output_pkl_stream)
        output_pkl_stream.close()


        #Some parameter variants & output to pkl
        advancedOpts = {'objective': 'chi2', 'profile': 2 }
        result = self.runSilent(pygsti.do_model_test, mdl_guess,
                                ds, std.target_model(), std.fiducials, std.fiducials,
                                std.germs, maxLens, advancedOptions=advancedOpts,
                                output_pkl = temp_files + "/driverModelTestResult2.pkl")

        with self.assertRaises(ValueError):
            advancedOpts = {'objective': 'foobar' }
            self.runSilent(pygsti.do_model_test, mdl_guess,
                           ds, std.target_model(), std.fiducials, std.fiducials,
                           std.germs, maxLens, advancedOptions=advancedOpts)
        with self.assertRaises(ValueError):
            advancedOpts = {'profile': 'foobar' }
            self.runSilent(pygsti.do_model_test, mdl_guess,
                           ds, std.target_model(), std.fiducials, std.fiducials,
                           std.germs, maxLens, advancedOptions=advancedOpts)



    def test_robust_data_scaling(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers2.dataset%s" % self.versionsuffix)
        mdl_guess = std.target_model().depolarize(op_noise=0.01,spam_noise=0.01)

        #lower bad-fit threshold to zero to trigger bad-fit additional processing
        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_long_sequence_gst,
                                ds, std.target_model(), std.fiducials, std.fiducials,
                                std.germs, maxLens, advancedOptions={'badFitThreshold': -100,
                                                                     'onBadFit': ["do nothing","robust","Robust","robust+","Robust+"]})

        with self.assertRaises(ValueError):
            self.runSilent(pygsti.do_long_sequence_gst,
                           ds, std.target_model(), std.fiducials, std.fiducials,
                           std.germs, maxLens, advancedOptions={'badFitThreshold': -100,
                                                                'onBadFit': ["foobar"]})


    def test_stdpracticeGST(self):
        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        mdl_guess = std.target_model().depolarize(op_noise=0.01,spam_noise=0.01)

        #lower bad-fit threshold to zero to trigger bad-fit additional processing
        maxLens = self.maxLens
        result = self.runSilent(pygsti.do_stdpractice_gst,
                                ds, std.target_model(), std.fiducials, std.fiducials,
                                std.germs, maxLens, modes="TP,CPTP,Test,Target",
                                modelsToTest = {"Test": mdl_guess},
                                comm=None, memLimit=None, verbosity=5)
        pygsti.report.create_standard_report(result, temp_files + "/full_report_stdpractice",
                                             "Std Practice Test Report", verbosity=2)

        #with string args, gaugeOptTarget, output pkl, and advanced options
        myGaugeOptSuiteDict = {
            'MyGaugeOpt': {
                'itemWeights': {'gates': 1, 'spam': 0.0001},
                'targetModel': std.target_model() # to test overriding internal target model (prints a warning)
            }
        }
        result = self.runSilent(pygsti.do_stdpractice_gst,
                                temp_files + "/driver_test_dataset.txt",
                                temp_files + "/driver.model",
                                temp_files + "/driver_fiducials.txt",
                                temp_files + "/driver_fiducials.txt",
                                temp_files + "/driver_germs.txt",
                                maxLens, modes="TP", comm=None, memLimit=None, verbosity=5,
                                gaugeOptTarget = mdl_guess,
                                gaugeOptSuite = myGaugeOptSuiteDict,
                                output_pkl = temp_files + "/driver_results1.pkl",
                                advancedOptions={ 'all': {
                                    'objective': 'chi2',
                                    'badFitThreshold': -100, # so we create a robust estimate and convey
                                    'onBadFit': ["robust"]   # guage opt to it.
                                } } )

        # test running just Target mode, and writing to an output *stream*
        out_pkl_stream = open(temp_files + "/driver_results2.pkl",'wb')
        self.runSilent(pygsti.do_stdpractice_gst,
                       ds, std.target_model(), std.fiducials, std.fiducials,
                       std.germs, maxLens, modes="Target", output_pkl=out_pkl_stream)
        out_pkl_stream.close()

        # test invalid mode
        with self.assertRaises(ValueError):
            self.runSilent(pygsti.do_stdpractice_gst,
                           ds, std.target_model(), std.fiducials, std.fiducials,
                           std.germs, maxLens, modes="Foobar")

    def test_gaugeopt_suite_to_dict(self):

        mdl_target_trivialgg = std2Q.target_model()
        mdl_target_trivialgg.default_gauge_group = pygsti.obj.TrivialGaugeGroup(4)

        d = pygsti.drivers.gaugeopt_suite_to_dictionary("single", std.target_model(), verbosity=1)
        d2 = pygsti.drivers.gaugeopt_suite_to_dictionary(d, std.target_model(), verbosity=1) #with dictionary - basically a pass-through

        d = pygsti.drivers.gaugeopt_suite_to_dictionary(["varySpam", "varySpamWt", "varyValidSpamWt", "toggleValidSpam","none"],
                                                        std.target_model(), verbosity=1)
        d = pygsti.drivers.gaugeopt_suite_to_dictionary(["varySpam", "varySpamWt", "varyValidSpamWt", "toggleValidSpam", "unreliable2Q"],
                                                        mdl_target_trivialgg, verbosity=1)

        d = pygsti.drivers.gaugeopt_suite_to_dictionary(["single","unreliable2Q"], std.target_model(), verbosity=1) #non-2Q gates
        d = pygsti.drivers.gaugeopt_suite_to_dictionary(["single","unreliable2Q"], std2Q.target_model(), verbosity=1)

        advOpts = {'all': {'unreliableOps': ['Gx','Gcnot']}}
        d = pygsti.drivers.gaugeopt_suite_to_dictionary(["single","unreliable2Q"], std2Q.target_model(), advOpts, verbosity=1)
        d = pygsti.drivers.gaugeopt_suite_to_dictionary(["varySpam","unreliable2Q"], std2Q.target_model(), advOpts, verbosity=1)

        with self.assertRaises(ValueError):
            pygsti.drivers.gaugeopt_suite_to_dictionary(["foobar"], std.target_model(), verbosity=1)

    def test_bootstrap(self):

        def dbsizes(mdl, title): #additional model debugging
            print(title)
            for l,o in mdl.operations.items(): print(l,":",o.num_params(),o.gpindices)
            for l,o in mdl.preps.items(): print(l,":",o.num_params(),o.gpindices)
            for l,o in mdl.povms.items(): print(l,":",o.num_params(),o.gpindices)
            print("")

        dbsizes(std.target_model(),"Orig target")

        ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/drivers.dataset%s" % self.versionsuffix)
        tp_target = std.target_model()
        dbsizes(tp_target,"target copy")
        tp_target.set_all_parameterizations("TP")
        dbsizes(tp_target,"TP target")

        print("LGST------------------")
        mdl = pygsti.do_lgst(ds, std.fiducials, std.fiducials, targetModel=tp_target, svdTruncateTo=4, verbosity=0)

        dbsizes(mdl, "LGST result")

        bootds_p = pygsti.drivers.make_bootstrap_dataset(
            ds,'parametric', mdl, seed=1234 )
        bootds_np = pygsti.drivers.make_bootstrap_dataset(
            ds,'nonparametric', seed=1234 )

        with self.assertRaises(ValueError):
            pygsti.drivers.make_bootstrap_dataset(ds,'foobar', seed=1)
              #bad generationMethod
        with self.assertRaises(ValueError):
            pygsti.drivers.make_bootstrap_dataset(ds,'parametric', seed=1)
              # must specify model for parametric mode
        with self.assertRaises(ValueError):
            pygsti.drivers.make_bootstrap_dataset(ds,'nonparametric',mdl,seed=1)
              # must *not* specify model for nonparametric mode


        maxLengths = [0] #just do LGST strings to make this fast...
        bootgs_p = pygsti.drivers.make_bootstrap_models( # self.runSilent(
            2, ds, 'parametric', std.fiducials, std.fiducials,
            std.germs, maxLengths, inputModel=mdl,
            returnData=False)

        dbsizes(bootgs_p[0],"bootgs_p[0]")

        #again, but with a specified list
        custom_strs = pygsti.construction.make_lsgst_lists(
            mdl, std.fiducials, std.fiducials, std.germs, [1])
        bootgs_p_custom = self.runSilent(pygsti.drivers.make_bootstrap_models,
                                         2, ds, 'parametric', None,None,None,None,
                                         lsgstLists=custom_strs, inputModel=mdl,
                                         returnData=False)

        default_maxLens = [0]+[2**k for k in range(10)]
        circuits = pygsti.construction.make_lsgst_experiment_list(
            self.opLabels, self.fiducials, self.fiducials, self.germs,
            default_maxLens, fidPairs=None, truncScheme="whole germ powers")
        ds_defaultMaxLens = pygsti.construction.generate_fake_data(
            mdl, circuits, nSamples=10000, sampleError='round')

        bootgs_p_defaultMaxLens = \
            pygsti.drivers.make_bootstrap_models( #self.runSilent(
            2, ds_defaultMaxLens, 'parametric', std.fiducials, std.fiducials,
            std.germs, None, inputModel=mdl,
            returnData=False) #test when maxLengths == None

        bootgs_np, bootds_np2 = self.runSilent(
            pygsti.drivers.make_bootstrap_models,
            2, ds, 'nonparametric', std.fiducials, std.fiducials,
            std.germs, maxLengths, targetModel=mdl,
            returnData=True)

        with self.assertRaises(ValueError):
            pygsti.drivers.make_bootstrap_models(
                2, ds, 'parametric', std.fiducials, std.fiducials,
                std.germs, maxLengths,returnData=False)
                #must specify either inputModel or targetModel

        with self.assertRaises(ValueError):
            pygsti.drivers.make_bootstrap_models(
                2, ds, 'parametric', std.fiducials, std.fiducials,
                std.germs, maxLengths, inputModel=mdl, targetModel=mdl,
                returnData=False) #cannot specify both inputModel and targetModel


        self.runSilent(pygsti.drivers.gauge_optimize_model_list,
                       bootgs_p, std.target_model(), gateMetric = 'frobenius',
                       spamMetric = 'frobenius', plot=False)

        #Test plotting not impl -- b/c plotting was removed w/matplotlib removal
        with self.assertRaises(NotImplementedError):
            pygsti.drivers.gauge_optimize_model_list(
                bootgs_p, std.target_model(), gateMetric = 'frobenius',
                spamMetric = 'frobenius', plot=True)


        #Test utility functions -- just make sure they run for now...
        def gsFn(mdl):
            return mdl.get_dimension()

        tp_target = std.target_model()
        tp_target.set_all_parameterizations("TP")

        pygsti.drivers.mdl_stdev(gsFn, bootgs_p)
        pygsti.drivers.mdl_mean(gsFn, bootgs_p)
        #pygsti.drivers.to_vector(bootgs_p[0]) #removed

        pygsti.drivers.to_mean_model(bootgs_p, tp_target)
        pygsti.drivers.to_std_model(bootgs_p, tp_target)
        pygsti.drivers.to_rms_model(bootgs_p, tp_target)

        #Removed (unused)
        #pygsti.drivers.gateset_jtracedist(bootgs_p[0], tp_target)
        #pygsti.drivers.gateset_process_fidelity(bootgs_p[0], tp_target)
        #pygsti.drivers.gateset_diamonddist(bootgs_p[0], tp_target)
        #pygsti.drivers.gateset_decomp_angle(bootgs_p[0])
        #pygsti.drivers.gateset_decomp_decay_diag(bootgs_p[0])
        #pygsti.drivers.gateset_decomp_decay_offdiag(bootgs_p[0])
        #pygsti.drivers.spamrameter(bootgs_p[0])



if __name__ == "__main__":
    unittest.main(verbosity=2)
