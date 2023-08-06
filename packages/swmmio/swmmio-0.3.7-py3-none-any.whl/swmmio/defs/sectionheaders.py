#=================
#DEFINE INP HEADER THAT SHOULD BE REPLACED
#=================


inp_header_dict = {
    '[TITLE]':'blob',
    '[OPTIONS]':'Name Value',
    '[FILES]': 'Action FileType FileName',
    '[CONDUITS]': 'Name InletNode OutletNode Length ManningN InletOffset OutletOffset InitFlow MaxFlow',
    '[COORDINATES]': 'Name X Y',
    '[JUNCTIONS]': 'Name InvertElev MaxDepth InitDepth SurchargeDepth PondedArea',
    '[ORIFICES]': 'Name InletNode OutletNode OrificeType CrestHeight DischCoeff FlapGate OpenCloseTime',
    '[OUTFALLS]': 'Name InvertElev OutfallType StageOrTimeseries TideGate',
    '[STORAGE]': 'Name InvertElev MaxD InitDepth StorageCurve Coefficient Exponent Constant PondedArea EvapFrac SuctionHead Conductivity InitialDeficit',
    '[VERTICES]': 'Name X Y',
    '[WEIRS]': 'Name InletNode OutletNode WeirType CrestHeight DischCoeff FlapGate EndCon EndCoeff Surcharge  RoadWidth  RoadSurf',
    '[XSECTIONS]':'Link Shape Geom1 Geom2 Geom3 Geom4 Barrels',
    '[SUBCATCHMENTS]':'Name Raingage Outlet Area PercImperv Width PercSlope CurbLength SnowPack',
    '[SUBAREAS]':'Name N-Imperv N-Perv S-Imperv S-Perv PctZero RouteTo PctRouted',
    '[LOSSES]':'Link Inlet Outlet Average FlapGate',
    '[PUMPS]':'Name InletNode OutletNode PumpCurve InitStatus Depth ShutoffDepth',
    '[DWF]':'Node Parameter AverageValue TimePatterns',
    '[RAINGAGES]':'Name RainType TimeIntrv SnowCatch DataSourceType DataSourceName',
    '[INFILTRATION]':'Subcatchment Suction HydCon IMDmax',
    '[Polygons]':'Name X Y',
    '[REPORT]':'Param Status',
    '[TAGS]':'ElementType Name Tag',
    '[MAP]': 'x1 y1 x2 y2',
    '[CURVES]': 'Name Type X-Value Y-Value',
    #'[TIMESERIES]':'Name Date Time Value'
}

#=================
#DEFINE RPT HEADER THAT SHOULD BE REPLACED
#=================
rpt_header_dict={
    'Subcatchment Summary':"Name Area Width ImpervPerc SlopePerc RainGage Outlet",
    'Node Summary':"Name Type InvertEl MaxD PondedA ExternalInf",
    'Link Summary':'Name FromNode ToNode Type Length SlopePerc Roughness',
    'Cross Section Summary':'Name Shape DFull AreaFull HydRad MaxW NumBarrels FullFlow',
    'Subcatchment Runoff Summary':'Name TotalPrecip TotalRunon TotalEvap TotalInfil TotalRunoffIn TotalRunoffMG PeakRunoff RunoffCoeff',
    'Node Flooding Summary':'Name HoursFlooded MaxQ MaxDay MaxHr TotalFloodVol MaximumPondDepth',
    'Node Inflow Summary':'Name Type MaxLatInflow MaxTotalInflow MaxDay MaxHr LatInflowV TotalInflowV FlowBalErrorPerc XXX',
    'Node Surcharge Summary':'Name Type HourSurcharged MaxHeightAboveCrown MinDepthBelowRim',
    'Storage Volume Summary':'Name AvgVolume AvgPctFull EvapPctLoss ExfilPctLoss MaxVolume MaxPctFull MaxDay MaxFullHr MaxOutflow',
    'Node Depth Summary':'Name Type AvgDepth MaxNodeDepth MaxHGL MaxDay MaxHr MaxNodeDepthReported',
    'Link Flow Summary':'Name Type MaxQ MaxDay MaxHr MaxV MaxQPerc MaxDPerc',
    'Subcatchment Results':     'Date Time PrecipInchPerHour LossesInchPerHr RunoffCFS',
    'Node Results':             'Date Time InflowCFS FloodingCFS DepthFt HeadFt TSS TP TN',
    'Link Results':             'Date Time FlowCFS VelocityFPS DepthFt PercentFull',
}
