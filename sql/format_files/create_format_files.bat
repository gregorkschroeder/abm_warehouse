bcp ws.staging.airport_trips format nul -c -x -f airport_trips.xml -t, -S sql2014a8 -T
bcp ws.staging.crossborder_tours format nul -c -x -f crossborder_tours.xml -t, -S sql2014a8 -T
bcp ws.staging.crossborder_trips format nul -c -x -f crossborder_trips.xml -t, -S sql2014a8 -T
bcp ws.staging.internalexternal_trips format nul -c -x -f internalexternal_trips.xml -t, -S sql2014a8 -T
bcp ws.staging.visitor_tours format nul -c -x -f visitor_tours.xml -t, -S sql2014a8 -T
bcp ws.staging.visitor_trips format nul -c -x -f visitor_trips.xml -t, -S sql2014a8 -T