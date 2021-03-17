import grg_pssedata as pd
from .readfiles import read_case

def conversion_to_33(filename):
    case34 = read_case(filename)

    # Buses
    for idx, bus in enumerate(case34["BUSES"]):
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

    # Loads
    for idx, load in enumerate(case34["LOAD"]):
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
            intrpt=load["INTRP"]
        )
    # TODO send warning of missing DGENQ DGENF

    # Fixed Shunts
    for idx, fs in enumerate(case34["FIXED SHUNT"]):
        pd.struct.FixedShunt(
            index=idx,
            i=fs["I"],
            id=fs["ID"],
            status=fs["STATUS"],
            gl=fs["GL"],
            bl=fs["BL"]
        ) 

    # Generators
    for idx, gen in enumerate(case34["GENERATOR"]):
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
            o2=gen["O2"],
            f2=gen["F2"],
            o3=gen["O3"],
            f3=gen["F3"],
            o4=gen["O4"],
            f4=gen["F4"],
            wmod=gen["WMOD"],
            wpf=gen["WPF"],
            nreg=gen["NREG"]
        )

    # Branches
    for idx, br in enumerate(case34["BRANCH"]):
        pd.struct.Branch(
            index=idx,
            i=br["I"],
            j=br["J"],
            ckt=br["CKT"],
            r=br["R"],
            x=br["X"],
            b=br["B"],
            name=br["NAME"],
            ratea=br["RATE1"],
            rateb=br["RATE2"],
            ratec=br["RATE3"],
            gi=br["GI"],
            bi=br["BI"],
            gj=br["GJ"],
            bj=br["BJ"],
            st=br["ST"],
            met=br["MET"],
            len=br["LEN"],
            o1=br["O1"],
            f1=br["F1"],
            o2=br["O2"],
            f2=br["F2"],
            o3=br["O3"],
            f3=br["F3"],
            o4=br["O4"],
            f4=br["F4"]
        )