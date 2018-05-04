docker run -v /eodata:/eodata:ro -v /tmp:/out:rw -v /DEM/CDEM:/home/ogc/.snap/auxdata/dem/CDEM:rw ogc/eoephackaton /opt/snap/bin/gpt -e /S1_Cal_Deb_ML_Spk_TC_cmd.xml -Pinputdata=/eodata/Sentinel-1/SAR/SLC/2017/06/17/S1A_IW_SLC__1SDH_20170617T145454_20170617T145521_017075_01C740_27DC.SAFE -Poutputdata=/out/S1result

