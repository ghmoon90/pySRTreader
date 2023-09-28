import sys
import numpy
import lxml
import re
from bs4 import BeautifulSoup

if __name__ == "__main__":

    lat = []
    lon = []
    alt = []
    relalt= []
    t_stamp = []
    date = ''
    
    file_title = re.split('\\|/',sys.argv[1].replace('.srt',''))[-1]
    
    with open( sys.argv[1] , "r")  as SRT_obj:
        doc_SRT = SRT_obj.read()
        bs_obj = BeautifulSoup(doc_SRT, "lxml", from_encoding='utf-8')
        
        for fonttag in bs_obj.find_all('font'):
            lines= re.split("\n",fonttag.text)
            time_temp = lines[1].replace(" ",":").split(":")
            date = time_temp[0]
            t_sec = float(time_temp[1]) * 3600 + float(time_temp[2]) * 60 + float(time_temp[3])
            
            dict_temp = eval( '{'+lines[2].replace('] [', ",\"").replace('[', "\"").replace(']', " ").replace(':', "\":").replace('abs_alt', ",\"abs_alt").replace('default', "\"default\"")+'}')
            lat.append(float(dict_temp['latitude']))
            lon.append(float(dict_temp['longitude']))
            alt.append(float(dict_temp['abs_alt']))
            relalt.append(float(dict_temp['rel_alt']))
            t_stamp.append(t_sec)
            
            
         
    with open( file_title+'.dat' , "w+") as out_obj:
        
        out_obj.write( f"t_sec  lat     lon     rel_alt     abs_alt\n" )
        for idx in range(0,len(t_stamp)):
            out_obj.write( f"{t_stamp[idx]:.3f} {lat[idx]:.6f}  {lon[idx]:.6f}  {alt[idx]:.6f}  {relalt[idx]:.6f}\n" )