# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:16:42 2019

@author: Administrator
"""

import math


class CoordinateSystemConversion():
    '''
    该类主要实现对如下三种坐标系的相互转换
    WGS：标准坐标系
    GCJ：火星坐标系
    BD：百度坐标系
    '''
    def  __init__(self):
        self.earthR = 6378137.0
        self.__all__ = ['wgs2gcj', 'gcj2wgs', 'gcj2wgs_exact',
           'distance', 'gcj2bd', 'bd2gcj', 'wgs2bd', 'bd2wgs']
    
    def outOfChina(self, lng, lat):
        return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)
    
    
    def transform(self, x, y):
    	xy = x * y
    	absX = math.sqrt(abs(x))
    	xPi = x * math.pi
    	yPi = y * math.pi
    	d = 20.0*math.sin(6.0*xPi) + 20.0*math.sin(2.0*xPi)
    
    	lat = d
    	lng = d
    
    	lat += 20.0*math.sin(yPi) + 40.0*math.sin(yPi/3.0)
    	lng += 20.0*math.sin(xPi) + 40.0*math.sin(xPi/3.0)
    
    	lat += 160.0*math.sin(yPi/12.0) + 320*math.sin(yPi/30.0)
    	lng += 150.0*math.sin(xPi/12.0) + 300.0*math.sin(xPi/30.0)
    
    	lat *= 2.0 / 3.0
    	lng *= 2.0 / 3.0
    
    	lat += -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*xy + 0.2*absX
    	lng += 300.0 + x + 2.0*y + 0.1*x*x + 0.1*xy + 0.1*absX
    
    	return lng, lat
    
    
    def delta(self, lng, lat):
        ee = 0.00669342162296594323
        dLng, dLat = self.transform(lng-105.0, lat-35.0)
        radLat = lat / 180.0 * math.pi
        magic = math.sin(radLat)
        magic = 1 - ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((self.earthR * (1 - ee)) / (magic * sqrtMagic) * math.pi)
        dLng = (dLng * 180.0) / (self.earthR / sqrtMagic * math.cos(radLat) * math.pi)
        return dLng, dLat


class transformMethod(CoordinateSystemConversion):
    '''
    该子类实现'wgs2gcj', 'gcj2wgs', 'gcj2wgs_exact', 'distance', 'gcj2bd', 'bd2gcj', 'wgs2bd', 'bd2wgs'
    共八种方法的转换
    输入demo：gcj2bd(113.318488, 23.121128)
    输出：
    '''
    def __init__(self):
        super(transformMethod, self).__init__()
        
        
    def wgs2gcj(self, wgsLng, wgsLat):#
        if self.outOfChina(wgsLng, wgsLat):
            return wgsLng, wgsLat
        else:
            dlng, dlat = self.delta(wgsLng, wgsLat)
            return str(round(wgsLng + dlng, 6))+','+str(round(wgsLat + dlat, 6))
    
    
    def gcj2wgs(self, gcjLng, gcjLat):
        if self.outOfChina(gcjLng, gcjLat):
            return gcjLng, gcjLat
        else:
            dlng, dlat = self.delta(gcjLng, gcjLat)
#            return str(round(gcjLng - dlng, 6))+','+str(round(gcjLat - dlat, 6))
            return str(round(gcjLng - dlng, 6))+','+str(round(gcjLat - dlat, 6))
#            return round(gcjLng - dlng, 6), round(gcjLat - dlat, 6)
    
    
    def gcj2wgs_exact(self, gcjLng, gcjLat):
        initDelta = 0.01
        threshold = 0.000001
        dLat = dLng = initDelta
        mLat = gcjLat - dLat
        mLng = gcjLng - dLng
        pLat = gcjLat + dLat
        pLng = gcjLng + dLng
        for i in range(30):
            wgsLat = (mLat + pLat) / 2
            wgsLng = (mLng + pLng) / 2
            tmplng, tmplat = self.wgs2gcj(wgsLng, wgsLat)
            dLat = tmplat - gcjLat
            dLng = tmplng - gcjLng
            if abs(dLat) < threshold and abs(dLng) < threshold:
                return wgsLng, wgsLat
            if dLat > 0:
                pLat = wgsLat
            else:
                mLat = wgsLat
            if dLng > 0:
                pLng = wgsLng
            else:
                mLng = wgsLng
        return str(round(wgsLng, 6))+','+str(round(wgsLat, 6))
    
    
    def distance(self, latA, lngA, latB, lngB):
        pi180 = math.pi / 180
        arcLatA = latA * pi180
        arcLatB = latB * pi180
        x = (math.cos(arcLatA) * math.cos(arcLatB) *
             math.cos((lngA - lngB) * pi180))
        y = math.sin(arcLatA) * math.sin(arcLatB)
        s = x + y
        if s > 1:
            s = 1
        if s < -1:
            s = -1
        alpha = math.acos(s)
        distance = alpha * self.earthR
        return distance
    
    
    def gcj2bd(self, gcjLng, gcjLat):
        if self.outOfChina(gcjLng, gcjLat):
            return gcjLng, gcjLat
    
        x = gcjLng
        y = gcjLat
        z = math.hypot(x, y) + 0.00002 * math.sin(y * math.pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * math.pi)
        bdLng = z * math.cos(theta) + 0.0065
        bdLat = z * math.sin(theta) + 0.006
        return str(round(bdLng, 6))+','+str(round(bdLat, 6))
    
    
    def bd2gcj(self, bdLng, bdLat):
        if self.outOfChina(bdLng, bdLat):
            return bdLng, bdLat
    
        x = bdLng - 0.0065
        y = bdLat - 0.006
        z = math.hypot(x, y) - 0.00002 * math.sin(y * math.pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * math.pi)
        gcjLng = z * math.cos(theta)
        gcjLat = z * math.sin(theta)
        return str(round(gcjLng, 6))+','+str(round(gcjLat, 6))
    

    def wgs2bd(self,wgsLng, wgsLat):
        st = self.wgs2gcj(wgsLng, wgsLat)
        gcjlng = float(st.split(',')[0])
        gcjlat = float(st.split(',')[1])
        return self.gcj2bd(gcjlng, gcjlat)
    
    
    def bd2wgs(self, bdLng, bdLat):
        st = self.bd2gcj(bdLng, bdLat)
        gcjlng = float(st.split(',')[0])
        gcjlat = float(st.split(',')[1])
        return self.gcj2wgs(gcjlng, gcjlat)
    
    
