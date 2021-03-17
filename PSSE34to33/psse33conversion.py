import grg_pssedata as pd
import warnings
from .readfiles import read_case

def _filter(dictionary: dict):
    return {k: v.replace('\"', '') for k, v in dictionary.items() if v is not None}

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
        warnings.warn("LOAD: Lose DGENQ and DGENF data")

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
        warnings.warn("GENERATOR: Lose NREG data")

    # Branches
    branches = []
    for idx, br in enumerate(case34["BRANCH"]+case34["SYSTEM SWITCHING DEVICE"]):
        br = _filter(br) # Filter None
        branches.append(
            pd.struct.Branch(
                index=idx,
                i=br.get("I"),
                j=br.get("J"),
                ckt=br.get("CKT"),
                r=br.get("R", 0.),
                x=br.get("X", 0.0001),
                b=br.get("B", 0),
                ratea=br.get("RATE1"),
                rateb=br.get("RATE2"),
                ratec=br.get("RATE3"),
                gi=br.get("GI", 0),
                bi=br.get("BI", 0),
                gj=br.get("GJ", 0),
                bj=br.get("BJ", 0),
                st=br.get("STAT"),
                met=br.get("MET"),
                len=br.get("LEN", 0),
                o1=br.get("O1", 0),
                f1=br.get("F1", 1),
                o2=br.get("O2", 0),
                f2=br.get("F2", 1),
                o3=br.get("O3", 0),
                f3=br.get("F3", 1),
                o4=br.get("O4", 0),
                f4=br.get("F4", 1)
            )
        )
        warnings.warn("BRANCHES: Lose severals ratings RATE4...RATE12 data")
        warnings.warn("SWITCHES: Converted to zero impedance branch")

    # Transformers
    transformers=[]
    for idx, transformer in enumerate(case34["TRANSFORMER"]):
        three_winding = transformer[0]["CKT"] == '0'
        # First Line
        p1 = _filter(transformer[0])
        pfl = pd.struct.TransformerParametersFirstLine(
            i=p1["I"],
            j=p1["J"],
            k=p1["K"],
            ckt=p1["CKT"],
            cw=p1["CW"],
            cz=p1["CZ"],
            cm=p1["CM"],
            mag1=p1["MAG1"],
            mag2=p1["MAG2"],
            nmetr=p1["NMETR"],
            name=["NAME"],
            stat=p1["STAT"],
            o1=p1.get("O1", 0),
            f1=p1.get("F1", 0),
            o2=p1.get("O2", 0),
            f2=p1.get("F2", 0),
            o3=p1.get("O3", 0),
            f3=p1.get("F3", 0),
            o4=p1.get("O4", 0),
            f4=p1.get("F4", 0),
            vecgrp=p1.get("VECGRP"),
        )
        # Second Line
        p2 = _filter(transformer[1])
        if three_winding:
            psl = pd.struct.TransformerParametersSecondLine(
                r12=p2["R1-2"],
                x12=p2["X1-2"],
                sbase12=p2["SBASE1-2"],
                r23=p2["R2-3"],
                x23=p2["X2-3"],
                sbase23=p2["SBASE2-3"],
                r31=p2["R3-1"],
                x31=p2["X3-1"],
                sbase31=p2["SBASE3-1"],
                vmstar=p2["VMSTAR"],
                anstar=p2["ANSTAR"]
            )
        else:
            psl = pd.struct.TransformerParametersSecondLineShort(
                r12=p2["R1-2"],
                x12=p2["X1-2"],
                sbase12=p2["SBASE1-2"]
            )
        # Winding One
        l1 = _filter(transformer[2])
        w1 = pd.struct.TransformerWinding(
            index=1,
            windv=l1["WINDV1"],
            nomv=l1["NOMV1"],
            ang=l1["ANG1"],
            rata=l1["RATE1-1"],
            ratb=l1["RATE1-2"],
            ratc=l1["RATE1-3"],
            cod=l1["COD1"],
            cont=l1["CONT1"],
            rma=l1["RMA1"],
            rmi=l1["RMI1"],
            vma=l1["VMA1"],
            vmi=l1["VMI1"],
            ntp=l1["NTP1"],
            tab=l1["TAB1"],
            cr=l1["CR1"],
            cx=l1["CX1"],
            cnxa=l1["CNXA1"]
        )
        # Winding Two
        l2 = _filter(transformer[3])
        if three_winding:
            w2 = pd.struct.TransformerWinding(
                index=2,
                windv=l2["WINDV2"],
                nomv=l2["NOMV2"],
                ang=l2["ANG2"],
                rata=l2["RATE2-1"],
                ratb=l2["RATE2-2"],
                ratc=l2["RATE2-3"],
                cod=l2["COD2"],
                cont=l2["CONT2"],
                rma=l2["RMA2"],
                rmi=l2["RMI2"],
                vma=l2["VMA2"],
                vmi=l2["VMI2"],
                ntp=l2["NTP2"],
                tab=l2["TAB2"],
                cr=l2["CR2"],
                cx=l2["CX2"],
                cnxa=l2["CNXA2"]
            )
        else:
            w2 = pd.struct.TransformerWindingShort(
                index=2,
                windv=l2["WINDV2"],
                nomv=l2["NOMV2"],
            )
        # Winding Three
        l3 = _filter(transformer[4])
        if three_winding:
            w3 = pd.struct.TransformerWinding(
                index=3,
                windv=l3["WINDV3"],
                nomv=l3["NOMV3"],
                ang=l3["ANG3"],
                rata=l3["RATE3-1"],
                ratb=l3["RATE3-2"],
                ratc=l3["RATE3-3"],
                cod=l3["COD3"],
                cont=l3["CONT3"],
                rma=l3["RMA3"],
                rmi=l3["RMI3"],
                vma=l3["VMA3"],
                vmi=l3["VMI3"],
                ntp=l3["NTP3"],
                tab=l3["TAB3"],
                cr=l3["CR3"],
                cx=l3["CX3"],
                cnxa=l3["CNXA3"]
            )
        if three_winding:
            transformer.append(pd.struct.ThreeWindingTransformer(idx, p1, p2, w1, w2, w3))
        else:
            transformer.append(pd.struct.TwoWindingTransformer(idx, p1, p2, w1, w2))

    # Areas
    areas=[]
    for idx, ar in enumerate(case34["AREA"]):
        areas.append(
            pd.struct.Area(
                i=ar["I"],
                isw=ar["ISW"],
                pdes=ar["PDES"],
                ptol=ar["PTOL"],
                arnam=ar["ARNAME"]
            )
        )


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

    # TODO: add this
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