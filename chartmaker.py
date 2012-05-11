#! /usr/bin/python
'''
Program loads pickled data of NMAP scans and parses them into GoogleCharts API html webpage for visualization
Writes both pie.html and bar.html to disk
'''


import cPickle as pickle
webcounter = 0
SSLwebcounter=0
Web8080=0
Windows135=0
Windows139=0
Windows445=0
Windows3389=0

dump = pickle.load(open('saveNewDict.2012-05-10'))
    
for item in dump.items():
    if len(item[1][1])>0: print item

for item in dump.items():
    dnsName = item[0]
    ipPorts = item[1]
    ipaddress = item[1][0]
    ports = item[1][1]
    if len(ports)>0:
        print
        print dnsName,ipaddress
        for i in range(len(ports)):
            print '*'*100
            print ipaddress, ports
        if '80/tcp' in ports: 
            webcounter += 1
        if '443/tcp' in ports: 
            SSLwebcounter +=1
        if '8080/tcp' in ports:
            Web8080 +=1
        if '135/tcp' in ports: 
            Windows135 += 1
        if '139/tcp' in ports: 
            Windows139 +=1
        if '445/tcp' in ports:
            Windows445 +=1
        if '3389/tcp' in ports:
            Windows3389 +=1

wList = ['Webservers',webcounter]
sslList = ['SSL Boxes',SSLwebcounter]
web8080List = ['Web8080',Web8080]
W135List = ['Windows135',Windows135]
W139List = ['Windows139',Windows139]
W445List = ['Windows445',Windows445]
W3389List = ['RDP3389',Windows3389]

htmlCodeStart = '''
<html>
  <head>

    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1.0', {'packages':['corechart']});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Type');
        data.addColumn('number', 'Servers');
        data.addRows(['''



htmlCodePieChart = ''']);
        var options = {'title':'Distribution External <EnterCompany>',
                       'width':400,
                       'height':300};
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
    <div id="chart_div"></div>
  </body>
</html>
'''


htmlCodeBarChart = '''
]);
        var options = {'title':'Distribution External <EnterCompany>',
                       'width':400,
                       'height':300};
        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
    <div id="chart_div"></div>
  </body>
</html>
'''

# this cats the Pie together
makePagePie = htmlCodeStart+str(wList)+','+str(W135List)+','+str(W139List)+','+str(W445List)+','+str(sslList)+','+str(web8080List)+','+str(W3389List)+htmlCodePieChart

# this cats the Bar together
makePageBar = htmlCodeStart+str(wList)+','+str(W135List)+','+str(W139List)+','+str(W445List)+','+str(sslList)+','+str(web8080List)+','+str(W3389List)+htmlCodeBarChart

#open file
fh = open('pie.html', 'w')
fd = open('bar.html', 'w')

#write file
fh.write(makePagePie)
fd.write(makePageBar)

#close handles
fh.close()
fd.close()
