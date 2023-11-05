q1=0;q2=0;q3=0;q4=0;
l1=4.5;  %cm
l2=10.5;
l3=10.5;
l4=9.0;
q=[q1 q2 q3 q4];

M10=transl(0,0,7.3);
M21=mtheslabon(q(1), l1, pi/2, 0);
M32=mtheslabon(q(2)+pi/2,0,0,l2);
M43=mtheslabon(q(3),0,0,l3);
M54=mtheslabon(q(4),0,0,l4);
MTCP5=troty(pi/2)*trotz(pi/2);
mtotal=M10*M21*M32*M43*M54*MTCP5

P1(1)=Link('revolute','d',l1,'alpha',pi/2,'a',0,'qlim',pi/180*[-180 180]);
P1(2)=Link('revolute','d',0,'alpha',0,'a',l2,'qlim',pi/180*[-150 150],'offset', pi/2;
P1(3)=Link('revolute','d',0,'alpha',0,'a',l3,'qlim',pi/180*[-150 150]);
P1(4)=Link('revolute','d',0,'alpha',0,'a',l4,'qlim',pi/180*[-150 150]);

phantom=SerialLink(P1,'name','Phantom');
phantom.tool=troty(pi/2)*trotz(pi/2);
phantom.base=transl(0,0,7.3);
phantom.plot(q,'workspace',[-40 40 -40 40 -5 40],'noa')
phantom.teach
phantom.fkine(q)
view([135 19])


function mth=mtheslabon(theta,d,alfa,a)
    mth=[cos(theta) -sin(theta)*cos(alfa) sin(theta)*sin(alfa) a*cos(theta);
        sin(theta) cos(theta)*cos(alfa) -cos(theta)*sin(alfa) a*sin(theta);
        0 sin(alfa) cos(alfa) d;
        0 0 0 1];
    mth=round(mth,4);
end
