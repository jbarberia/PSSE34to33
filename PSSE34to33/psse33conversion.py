import grg_pssedata as pd
from .readfiles import read_case

def conversion_to_33(filename):
    case34 = read_case(filename)

    # Buses
    buses = []
    for idx, bus in enumerate(case34["BUS"]):
        buses.append(
            pd.struct.Bus(
                i=bus["I"],
                name=bus["NAME"],
                basekv=bus["BASKV"],
                ide=bus["IDE"],
                area=bus["AREA"],
                zone=bus["ZONE"],
                owner=bus["OWNER"],
                vm=bus["VM"],
                va=bus["VA"],
                nvhi=bus["NVHI"],
                nvlo=bus["NVLO"],
                evhi=bus["EVHI"],
                evlo=bus["EVLO"]
            )
        ) 

    # Loads
    loads = []
    for idx, load in enumerate(case34["LOAD"]):
        loads.append(
            pd.struct.Load(
                index = idx,
                i=load["I"],
                id=load["ID"],
                status=load["STAT"],
                area=load["AREA"],
                zone=load["ZONE"],
                pl=load["PL"],
                ql=load["QL"],
                ip=load["IP"],
                iq=load["IQ"],
                yp=load["YP"],
                yq=load["YQ"],
                owner=load["OWNER"],
                scale=load["SCALE"],
                intrpt=load["INTRPT"]
            )
        )
    # TODO send warning of missing DGENQ DGENF

    # Fixed Shunts
    fixed_shunts = []
    for idx, fs in enumerate(case34["FIXED SHUNT"]):
        fixed_shunts.append(
            pd.struct.FixedShunt(
                index=idx,
                i=fs["I"],
                id=fs["ID"],
                status=fs["STATUS"],
                gl=fs["GL"],
                bl=fs["BL"]
            ) 
        )

    # Generators
    generators = []
    for idx, gen in enumerate(case34["GENERATOR"]):
        generators.append(
            pd.struct.Generator(
                index=idx,
                i=gen["I"],
                id=gen["ID"],
                pg=gen["PG"],
                qg=gen["QG"],
                qt=gen["QT"],
                qb=gen["QB"],
                vs=gen["VS"],
                ireg=gen["IREG"],
                mbase=gen["MBASE"],
                zr=gen["ZR"],
                zx=gen["ZX"],
                rt=gen["RT"],
                xt=gen["XT"],
                gtap=gen["GTAP"],
                stat=gen["STAT"],
                rmpct=gen["RMPCT"],
                pt=gen["PT"],
                pb=gen["PB"],
                o1=gen["O1"],
                f1=gen["F1"],
                o2=gen["O2"] if gen["O2"] else 0,
                f2=gen["F2"] if gen["F2"] else 1,
                o3=gen["O3"] if gen["O3"] else 0,
                f3=gen["F3"] if gen["F3"] else 1,
                o4=gen["O4"] if gen["O4"] else 0,
                f4=gen["F4"] if gen["F4"] else 1,
                wmod=gen["WMOD"] if gen["WMOD"] else 0,
                wpf=gen["WPF"] if gen["WPF"] else 1.,
            )
        )
        # TODO lost NREG

    # Branches
    branches = []
    for idx, br in enumerate(case34["BRANCH"]):
        branches.append(
            pd.struct.Branch(
                index=idx,
                i=br["I"],
                j=br["J"],
                ckt=br["CKT"],
                r=br["R"],
                x=br["X"],
                b=br["B"],
                ratea=br["RATE1"],
                rateb=br["RATE2"],
                ratec=br["RATE3"],
                gi=br["GI"],
                bi=br["BI"],
                gj=br["GJ"],
                bj=br["BJ"],
                st=br["STAT"],
                met=br["MET"],
                len=br["LEN"],
                o1=br["O1"],
                f1=br["F1"],
                o2=br["O2"] if br["O2"] else 0,
                f2=br["F2"] if br["F2"] else 0,
                o3=br["O3"] if br["O3"] else 0,
                f3=br["F3"] if br["F3"] else 0,
                o4=br["O4"] if br["O3"] else 0,
                f4=br["F4"] if br["F3"] else 0
            )
        )

    transformers=[]
    areas=[]
    tt_dc_lines=[]
    vsc_dc_lines=[]
    transformer_corrections=[]
    mt_dc_lines=[]
    line_groupings=[]
    zones=[]
    transfers=[]
    owners=[]
    facts=[]
    switched_shunts=[]
    gnes=[]
    induction_machine=[]

    ic=0
    sbase=100
    rev=33
    xfrrat=0
    nxfrat=0
    basfrq=50
    reacord1=0
    record2=0


    case33 = pd.struct.Case(
        ic, sbase, rev, xfrrat, nxfrat, basfrq, reacord1, record2,
        buses, loads, fixed_shunts, generators, branches,
        transformers, areas, tt_dc_lines, vsc_dc_lines, transformer_corrections, mt_dc_lines,
        line_groupings, zones, transfers, owners, facts, switched_shunts,
        gnes, induction_machine
    )
    return case33