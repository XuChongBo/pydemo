#!/usr/bin/env python
# -*- coding:utf-8 -*-


from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import codecs
from Stroke import Stroke
from flask import current_app


class Hanzi:
    @staticmethod
    def parse_from_file(svgfile):
        print svgfile, type(svgfile)
        tree = ElementTree.parse(svgfile)
        root = tree.getroot()
        for child in root:
            print child.tag, child.attrib
        rawStrokes = []
        for stroke in root.iter('{http://www.w3.org/2000/svg}polyline'):
            print stroke.attrib
            rawStroke = []
            for point in stroke.get('points').split():
                x,y = point.split(',')
                rawStroke.append([int(x),int(y)])
            rawStrokes.append(rawStroke)
        tag = root.get("hanzi")
        #root.get("stroke_num"),
        width = int(root.get("width")[:-2])
        height = int(root.get("height")[:-2])
        return Hanzi(tag, rawStrokes, width,height)
        current_app.hanzi_list

    def __init__(self, tag, rawStrokes, width, height):
        self.tag = tag
        self.width = width
        self.height = height
        self.rawStrokes = rawStrokes
        ## use for match or recoginze
        self.normalizedStrokes = []
        self.features = {'strokeNum':len(rawStrokes),'strokeDirections':[], 'strokeStarts':[], 'strokeEnds':[] , 'moveDirections':[]}
        # 
        self.calculate_features()

    # def numberToSVG(self, out, number, indent = 0):
    #     if self.numberPos:
    #         out.write("\t" * indent + '<text transform="matrix(1 0 0 1 %.2f %.2f)">%d</text>\n' % (self.numberPos[0], self.numberPos[1], number)) 

    # def toSVG(self, out, rootId, groupCpt, strCpt, indent = 0):
    #     pid = rootId + "-s" + str(strCpt[0])
    #     strCpt[0] += 1
    #     s = "\t" * indent + '<path id="kvg:%s"' % (pid,)
    #     if self.stype: s += ' kvg:type="%s"' % (self.stype,)
    #     if self.svg: s += ' d="%s"' % (self.svg)
    #     s += '/>\n'
    #     out.write(s)
    
    def __normalize_strokes(self):
        """
         * Normalises an array of strokes by converting their co-ordinates to range
         * from 0 to 1 in each direction. If the stroke bounding rectangle
         * has width or height 0, this will be handled so that it is at 0.5 in
         * the relevant position.
         * <p>
         * This works by constructing new stroke objects; strokes are final.
         * @param strokes Stroke array to convert
         * @return Resulting converted array
        """
        # Find range
        minX,minY,maxX,maxY = 10000000,10000000,-1,-1
        for stroke in self.rawStrokes:
            startX, startY, endX, endY =  stroke[0][0], stroke[0][1], stroke[-1][0], stroke[-1][1]
            if startX < minX:
                minX = startX
            if startX > maxX:
                maxX = startX
            if startY < minY:
                minY = startY
            if startY > maxY:
                maxY = startY
            
            if endX < minX:
                minX = endX
            if endX > maxX:
                maxX = endX
            if endY < minY:
                minY = endY
            if endY > maxY:
                maxY = endY
        current_app.logger.debug("minX=%s, maxX=%s, minY=%s, maxY=%s", minX, maxX, minY, maxY)
        #// Adjust max/min to avoid divide by zero
        if abs(minX - maxX) < 0.0000000001:
            #// Adjust by 1% of height
            adjust = abs(minY - maxY) / 100.0
            if adjust < 0.0000000001:
                adjust = 0.1
            minX -= adjust
            maxX += adjust
        if abs(minY - maxY) < 0.0000000001:
            # // Adjust by 1% of width
            adjust = abs(minX - maxX) / 100.0
            if adjust < 0.0000000001:
                adjust = 0.1
            minY -= adjust
            maxY += adjust
        
        # Now sort out a maximum scale factor, so that very long/thin kanji
        # don't get stretched to square
        xRange = abs(minX - maxX)
        yRange = abs(minY - maxY)
        if xRange > 5.0* yRange:
            adjust = (xRange - yRange) / 2
            minY -= adjust
            maxY += adjust
        elif yRange > 5.0 * xRange:
            adjust = (yRange - xRange) / 2
            minX -= adjust
            maxX += adjust

        current_app.logger.debug("after modify. minX=%s, maxX=%s, minY=%s, maxY=%s", minX, maxX, minY, maxY)
        #Convert all points according to range
        for stroke in self.rawStrokes:
            startX, startY, endX, endY =  stroke[0][0], stroke[0][1], stroke[-1][0], stroke[-1][1]
            self.normalizedStrokes.append( Stroke((startX - minX)*1.0 / (maxX - minX),
                        (startY - minY)*1.0 / (maxY - minY),
                        (endX - minX)*1.0 / (maxX - minX),
                        (endY - minY)*1.0 / (maxY - minY)) )

    def calculate_features(self):
        """
            Calculate the direction summary.
        """
        self.__normalize_strokes()
        # Find all the directions
        for i, stroke in enumerate(self.normalizedStrokes):
            self.features['strokeDirections'].append( stroke.getDirection() )
            self.features['strokeStarts'].append( stroke.getStartLocation() )
            self.features['strokeEnds'].append( stroke.getEndLocation() )
            if i>0:
                self.features['moveDirections'].append( stroke.getMoveDirection(self.normalizedStrokes[i-1]) )

    def _add_stroke_to_svg(self,stroke, svg, num):
        # <svg><users/>
        #component = SubElement( svg, 'g' )
        #n = len(stroke)
        # for idx in range(n-1):
        #     subelem_line = SubElement( component, 'line', stroke="red", x1=str(stroke[idx][0]), y1=str(stroke[idx][1]), x2=str(stroke[idx+1][0]), y2=str(stroke[idx+1][1]))
        #     subelem_line.set("stroke-width","1")
        points = ""
        for point in stroke:
            points += str(point[0])+","+str(point[1])+" "
        points = points[:-1]
        subelem_line = SubElement( svg, 'polyline', id=str(num), style="fill:none;stroke:red;stroke-width:1", points=points)
        #subelem_line.set("stroke-width","1")
        subelem_text = SubElement( svg, 'text',  transform="matrix(1 0 0 1 %s %s)" % (stroke[0][0],stroke[0][1]),style="font-size:8;fill:#808080")
        subelem_text.text = str(num)

    def save(self, filepath):
        #output_file = open( 'membership.xml', 'w' )
        #output_file = codecs.open( filepath, 'w','utf-8' )
        output_file = open( filepath, 'w')
        output_file.write( '<?xml version="1.0" encoding="UTF-8"?>' )
        
        # <svg/>
        svg = Element( 'svg', version="1.1", height=str(self.height)+"px", width=str(self.width)+"px", xmlns="http://www.w3.org/2000/svg")
        svg.set('hanzi',self.tag)
        svg.set('stroke_num',str(len(self.rawStrokes)))


        # <membership><groups><group><user/>
        # converted_strokes = []
        # scale = app.config['ImageWidth']*1.0/width
        # for stroke in rawStrokes:
        #     tmp = []
        #     for x,y in stroke:
        #         current_x = (x*scale)
        #         current_y = (y*scale)
        #         if len(tmp)>0 and current_x==tmp[-1][0] and current_y==tmp[-1][1]:
        #             continue
        #         tmp.append([current_x,current_y])
        #     converted_strokes.append(tmp)

        # # save svg
        # svg = simplesvg.SVG(app.config['ImageWidth'], app.config['ImageWidth'])

        for idx, stroke in enumerate(self.rawStrokes):
            self._add_stroke_to_svg(stroke,svg,idx+1)
            # n = len(stroke)
            # for idx in range(n-1):
            #     svg.line(stroke[idx][0], stroke[idx][1],stroke[idx+1][0], stroke[idx+1][1],stroke = "red", strokeWidth = app.config['StrokeWidth'])
        #print svg


        output_file.write( ElementTree.tostring( svg ) )
        output_file.close()


    

if __name__ == '__main__':
    h = Hanzi.parse("./test.svg")