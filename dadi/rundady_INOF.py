# generating the frequency spectrum
import sys
import os
import numpy
import dadi
from datetime import datetime
import Optimize_Functions
import Models_2D

model = int(sys.argv[1])

#===========================================================================
# Import data to create joint-site frequency spectrum
#===========================================================================
# load my data as dadi data dictionary
# subsample this many individuals
ss = {'COAST':40, 'FISHERIES':15}
dd = dadi.Misc.make_data_dict_vcf('./SNP_complete_thin1kb.vcf.gz',
                                  './SNP_complete_thin100kb.popfile.txt',
                                  subsample = ss)
#**************
#pop_ids is a list which should match the populations headers of your SNPs file columns
pop_ids=["FISHERIES", "COAST"]

#**************
#projection sizes, in ALLELES not individuals
proj = [30,80]

#Convert this dictionary into folded AFS object
#[polarized = False] creates folded spectrum object
fs = dadi.Spectrum.from_data_dict(dd, pop_ids=pop_ids, projections = proj, polarized = False)

#print some useful information about the afs or jsfs
print("\n\n============================================================================")
print("\nData for site frequency spectrum:\n")
print("Projection: {}".format(proj))
print("Sample sizes: {}".format(fs.sample_sizes))
print("Sum of SFS: {}".format(numpy.around(fs.S(), 2)))
print("\n============================================================================\n")



# copied from dadi pipeline
# these are the settings for the optimization routines

#create a prefix based on the population names to label the output files
#ex. Pop1_Pop2
prefix = "_".join(pop_ids)

#**************
#make sure to define your extrapolation grid size (based on your projections)
pts = [90,100,110]

#**************
#Set the number of rounds here
rounds = 5

#define the lists for optional arguments
#you can change these to alter the settings of the optimization routine
reps = [10,20,30,40,50]
maxiters = [3,5,10,15,20]
folds = [3,2,2,1,1]

#**************
#Indicate whether your frequency spectrum object is folded (True) or unfolded (False)
fs_folded = True


if model == 1:
    # Split into two populations, no migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "no_mig", Models_2D.no_mig, rounds, 3, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, T")
elif model == 2:
    # Split into two populations, with continuous symmetric migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sym_mig", Models_2D.sym_mig, rounds, 4, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m, T")
elif model == 3:
    # Split into two populations, with continuous asymmetric migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "asym_mig", Models_2D.asym_mig, rounds, 5, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m12, m21, T")
elif model == 4:
    # Split with continuous symmetric migration, followed by isolation.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "anc_sym_mig", Models_2D.anc_sym_mig, rounds, 5, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m, T1, T2")
elif model == 5:
    # Split with continuous asymmetric migration, followed by isolation.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "anc_asym_mig", Models_2D.anc_asym_mig, rounds, 6, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m12, m21, T1, T2")
elif model == 7:
    # Split with no gene flow, followed by period of continuous symmetrical gene flow.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_sym_mig", Models_2D.sec_contact_sym_mig, rounds, 5, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m, T1, T2")
elif model == 8:
    # Split with no gene flow, followed by period of continuous asymmetrical gene flow.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_asym_mig", Models_2D.sec_contact_asym_mig, rounds, 6, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m12, m21, T1, T2")
elif model == 9:
    # Split with no migration, then instantaneous size change with no migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "no_mig_size", Models_2D.no_mig_size, rounds, 6, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, T1, T2")
elif model == 10:
    # Split with symmetric migration, then instantaneous size change with continuous symmetric migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sym_mig_size", Models_2D.sym_mig_size, rounds, 7, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m, T1, T2")
elif model == 11:
    # Split with different migration rates, then instantaneous size change with continuous asymmetric migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "asym_mig_size", Models_2D.asym_mig_size, rounds, 8, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2")
elif model == 12:
    # Split with continuous symmetrical gene flow, followed by instantaneous size change with no migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "anc_sym_mig_size", Models_2D.anc_sym_mig_size, rounds, 7, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m, T1, T2")
elif model == 13:
    # Split with continuous asymmetrical gene flow, followed by instantaneous size change with no migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "anc_asym_mig_size", Models_2D.anc_asym_mig_size, rounds, 8, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2")
elif model == 14:
    # Split with no gene flow, followed by instantaneous size change with continuous symmetrical migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_sym_mig_size", Models_2D.sec_contact_sym_mig_size, rounds, 7, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m, T1, T2")
elif model == 15:
    # Split with no gene flow, followed by instantaneous size change with continuous asymmetrical migration.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_asym_mig_size", Models_2D.sec_contact_asym_mig_size, rounds, 8, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2")
elif model == 16:
    # Split into two populations, with continuous symmetric migration, rate varying across two epochs.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sym_mig_twoepoch", Models_2D.sym_mig_twoepoch, rounds, 6, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m1, m2, T1, T2")
elif model == 17:
    # Split into two populations, with continuous asymmetric migration, rate varying across two epochs.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "asym_mig_twoepoch", Models_2D.asym_mig_twoepoch, rounds, 8, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m12a, m21a, m12b, m21b, T1, T2")
elif model == 18:
    # Split with no gene flow, followed by period of continuous symmetrical migration, then isolation.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_sym_mig_three_epoch", Models_2D.sec_contact_sym_mig_three_epoch, rounds, 6, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m, T1, T2, T3")
elif model == 19:
    # Split with no gene flow, followed by period of continuous asymmetrical migration, then isolation.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_asym_mig_three_epoch", Models_2D.sec_contact_asym_mig_three_epoch, rounds, 7, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1, nu2, m12, m21, T1, T2, T3")
elif model == 20:
    # Split with no gene flow, followed by instantaneous size change with continuous symmetrical migration, then isolation.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_sym_mig_size_three_epoch", Models_2D.sec_contact_sym_mig_size_three_epoch, rounds, 8, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m, T1, T2, T3")
elif model == 21:
    # Split with no gene flow, followed by instantaneous size change with continuous asymmetrical migration, then isolation.
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "sec_contact_asym_mig_size_three_epoch", Models_2D.sec_contact_asym_mig_size_three_epoch, rounds, 9, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu1a, nu2a, nu1b, nu2b, m12, m21, T1, T2, T3")
elif model == 22:
    # Island: Vicariance with no migration.
    up = [10, 0.5]
    ps = [1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_no_mig", Models_2D.vic_no_mig, rounds, 2, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "T, s", in_upper=up, in_params=ps)
elif model == 23:
    # Island: Vicariance with ancient symmetric migration.
    up = [10, 10, 10, 0.5]
    ps = [1, 1, 1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_anc_sym_mig", Models_2D.vic_anc_sym_mig, rounds, 4, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "m, T1, T2, s", in_upper=up, in_params=ps)
elif model == 24:
    # Island: Vicariance with ancient asymmetric migration.
    up = [10, 10, 10, 10, 0.5]
    ps = [1, 1, 1, 1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_anc_asym_mig", Models_2D.vic_anc_asym_mig, rounds, 5, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "m12, m21, T1, T2, s", in_upper=up, in_params=ps)
elif model == 25:
    # Island: Vicariance with no migration, secondary contact with symmetric migration.
    up = [10, 10, 10, 0.5]
    ps = [1, 1, 1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_sec_contact_sym_mig", Models_2D.vic_sec_contact_sym_mig, rounds, 4, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "m, T1, T2, s", in_upper=up, in_params=ps)
elif model == 26:
    # Island: Vicariance with no migration, secondary contact with asymmetric migration.
    up = [10, 10, 10, 10, 0.5]
    ps = [1, 1, 1, 1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_sec_contact_asym_mig", Models_2D.vic_sec_contact_asym_mig, rounds, 5, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "m12, m21, T1, T2, s", in_upper=up, in_params=ps)
elif model == 27:
    # Island: Founder event with no migration.
    up = [20, 10, 0.5]
    ps = [1, 1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "founder_nomig", Models_2D.founder_nomig, rounds, 3, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu2, T, s", in_upper=up, in_params=ps)
elif model == 28:
    # Island: Founder event with symmetric migration.
    up = [20, 20, 10, 0.5]
    ps = [1, 1, 1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "founder_sym", Models_2D.founder_sym, rounds, 4, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu2, m, T, s", in_upper=up, in_params=ps)
elif model == 29:
    # Island: Founder event with asymmetric migration.
    up = [20, 20, 20, 10, 0.5]
    ps = [1, 1, 1, 1, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "founder_asym", Models_2D.founder_asym, rounds, 5, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu2, m12, m21, T, s", in_upper=up, in_params=ps)
elif model == 30:
    # Island: Vicariance, early unidirectional discrete admixture event (before drift).
    up = [10, 0.5, 0.99]
    ps = [1, 0.25, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_no_mig_admix_early", Models_2D.vic_no_mig_admix_early, rounds, 3, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "T, s, f", in_upper=up, in_params=ps)
elif model == 31:
    # Island: Vicariance, late unidirectional discrete admixture event (after drift).
    up = [10, 0.5, 0.99]
    ps = [1, 0.25, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_no_mig_admix_late", Models_2D.vic_no_mig_admix_late, rounds, 3, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "T, s, f", in_upper=up, in_params=ps)
elif model == 32:
    # Island: Vicariance, middle unidirectional discrete admixture event (between two drift events).
    up = [10, 10, 0.5, 0.99]
    ps = [1, 1, 0.25, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "vic_two_epoch_admix", Models_2D.vic_two_epoch_admix, rounds, 4, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "T1, T2, s, f", in_upper=up, in_params=ps)
elif model == 33:
    # Founder event with no migration, early unidirectional discrete admixture event (before drift).
    up = [20, 10, 0.5, 0.99]
    ps = [1, 1, 0.25, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "founder_nomig_admix_early", Models_2D.founder_nomig_admix_early, rounds, 4, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu2, T, s, f", in_upper=up, in_params=ps)
elif model == 34:
    # Founder event with no migration, late unidirectional discrete admixture event (after drift).
    up = [20, 10, 0.5, 0.99]
    ps = [1, 1, 0.25, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "founder_nomig_admix_late", Models_2D.founder_nomig_admix_late, rounds, 4, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu2, T, s, f", in_upper=up, in_params=ps)
elif model == 35:
    # Island: Founder event, middle unidirectional discrete admixture event (between two drift events).
    up = [20, 10, 10, 0.5, 0.99]
    ps = [1, 1, 1, 0.25, 0.25]
    Optimize_Functions.Optimize_Routine(fs, pts, prefix, "founder_nomig_admix_two_epoch", Models_2D.founder_nomig_admix_two_epoch, rounds, 5, fs_folded=fs_folded,
                                            reps=reps, maxiters=maxiters, folds=folds, param_labels = "nu2, T1, T2, s, f", in_upper=up, in_params=ps)
