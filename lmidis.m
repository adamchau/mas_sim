n=10; %dim of state vectors
m=4; %dim of input vector
N=3; %num of agents

% parameters of MAS
A=[0 0 9.389 0 0 0 9.389 0 0 0;
   0 0 0 -9.389 0 0 0 -9.389 0 0;
   0 0 0 0 1 0 0 0 0 0;
   0 0 0 0 0 1 0 0 0 0;
   0.2542 0 0 0 0 0 307.571 0 0 0;
   0 0 0 0 0 0 0 1172.4817 0 0;
   0 0 0 0 -1 0 -30.71 0.7713 0 0;
   0 0 0 0 0 -1 0.6168 -30.71 0 0;
   0 0 0 0 0 0 0 0 -2.055 0;
   0 2.982 0 0 0 0 0 0 -0.7076 -10.71]; 
B=[0 0 0 0;
   0 0 0 0;
   0 0 0 0;
   0 0 0 0;
   0 0 0 0;
   0 0 0 0;
   4.059 -0.0161 0 0;
   -0.01017 4.085 0 0;
   0 0 -13.11 0;
   0 0 3.749 26.9];
C=eye(n);
D=[-0.04743 0 0 0 0;
    0 -0.0763 0 0 0;
    0 0 0 0 0;
    0 0 0 0 0;
    0 0 0 -0.017408 0;
    0 0 0 -0.008981 -0.28926;
    0 0 0 0 0;
    0 0 0 0 0;
    0 0 0 0 0;
    0 0 0 0 0];
E=[1 0 0 0 0 0 0 0 0 0;
   0 1 0 0 0 0 0 0 0 0;
   0 1 0 0 0 0 0 0 0 0;
   1 0 0 0 0 0 0 0 0 0;
   0 1 0 0 0 0 0 0 0 0
    ];

x10=[2,1,-1.25,6,-3,1.4,-2.1,1.4,-6,2.4];
x20=[1.6,1.5,5,-2.5,3,-1.5,3.5,1.8,1,0.7];
x30=[-3,-1.4,1,4,1.7,1,-6,-1.5,-2.3,-4];
x0=[x10,x20,x30]';

% graph parameter 
DG=diag([2,1,1]);
AG=[0,1,1;1,0,0;1,0,0];
LG=DG-AG;
Di=zeros(1,N);
Di(1)=0.01;

% cost function parameter
Q=kron(LG+diag(Di),eye(n));
R=eye(N);
R=kron(R,eye(m));

% pre cal essential para 
lam=eig(LG+diag(Di));
r=1;
cp=1;

% lmi create and solve
if (size(A)==[n,n])&(size(B)==[n,m])
    display('dim checking:OK');
    setlmis([]);
    alpha=lmivar(1,[1,0]);
    X=lmivar(1,[n,1]);
    W=lmivar(2,[m n]);
    epsi=lmivar(1,[1,0]);
    for i=1:N
        lmiterm([i 1 1 X],A,1,'s');
        lmiterm([i 1 1 W],cp*lam(i)*B,1,'s');
        lmiterm([i 1 1 epsi],1,D*D');
        lmiterm([i 1 2 X],1,E');
        lmiterm([i 1 3 X],1,1);
        lmiterm([i 1 4 -W],cp*lam(i),1);
        lmiterm([i 2 2 epsi],-1,1);
        lmiterm([i 3 3 0],-lam(i)^(-1));
        lmiterm([i 4 4 0],-r^(-1));
    end
    if 1
        lmiterm([N+1 1 1 alpha],-1,1);
        lmiterm([N+1 1 2 0],x10);
        lmiterm([N+1 1 3 0],x20);
        lmiterm([N+1 1 4 0],x30);
        lmiterm([N+1 2 2 X],-1,1);
        lmiterm([N+1 3 3 X],-1,1);
        lmiterm([N+1 4 4 X],-1,1);
        lmiterm([-(N+2) 1 1 epsi],1,1);
        lmiterm([-(N+3) 1 1 X],1,1);
        gcclmisys=getlmis;
    end
    
    decn=decnbr(gcclmisys);
    c=zeros(decn,1);    
    for j=1:decn
        [alphaj]=defcx(gcclmisys,j,alpha);
        c(j)=alphaj;
    end
    options=[1e-5 0 0 0 0];
    [copt,xopt]=mincx(gcclmisys,c,options);
    X_sol=dec2mat(gcclmisys,xopt,X);
    W_sol=dec2mat(gcclmisys,xopt,W);
    epsi_sol=dec2mat(gcclmisys,xopt,epsi);
    K=W_sol/X_sol;
    J=x0'*kron(eye(N),inv(X_sol))*x0;
    P=inv(X_sol);
 
    for i=1:3
       if ~prod((eig((A+cp*lam(i)*B*K)'*P+P*(A+cp*lam(i)*B*K))<zeros(n,1)))
         disp('not stable')
         break;
       else
         disp('stable')
       end  
    end
    
    AN=kron(eye(N),A);
    BN=kron(eye(N),B);
    CN=kron(eye(N),C);
    KN=kron(cp*(LG+diag(Di)),K);
    PN=kron(eye(N),P);
    if prod((eig((AN+BN*KN)'*PN+PN*(AN+BN*KN))<zeros(n*N,1)))
        disp('stable')
    else
        disp('unstable')
    end
    status_his=[];
    input_his=[];
    J=0;
    dt=0.001;
    for t=0:dt:10
        xt=expm((AN+BN*KN)*t)*x0;
        ut=cp*KN*xt;
        J=J+dt*(xt'*Q*xt+ut'*R*ut);
        status_his=[status_his,xt];
        input_his=[input_his,ut];
    end
    statusnum=1;
    figure()
    plot(status_his(statusnum,:))
    hold on;
    plot(status_his(n+statusnum,:))
    plot(status_his(2*n+statusnum,:))
    hold off;
%     sys2=ss(AN+BN*KN,zeros(n*N,N*m),ones(n*N),zeros(n*N,N*m))
%     [T,x,y]=initial(sys2,x0)
    
    
%     options=[1e-5 0 0 0 0];
%     [tmin,xfeas]=feasp(gcclmisys,options);
%     X_sol2=dec2mat(gcclmisys,xopt,X);
%     W_sol2=dec2mat(gcclmisys,xopt,W);
%     K2=W_sol2*inv(X_sol2);
%     J2=x0'*kron(eye(N),inv(X_sol2))*x0;
    
else
    display('dim checking: ERROR')
end

save('lmitest2.mat','A','B','C','D','E','n','m','N','x10','x20','x30',...
    'Q','R','LG','Di','X_sol','W_sol','cp','K','J')

% setlmis([])
% X=lmivar(1,[1,0]);
% S=lmivar(1,[1,0]);
% lmiterm([1 1 1 X],1,A,'s');
% lmiterm([1 1 1 S],C',C);
% lmiterm([1 1 2 X],1,B);
% lmiterm([1 2 2 S],-1,1);
% 
% lmiterm([-2 1 1 X],1,1);
% 
% lmiterm([-3 1 1 S],1,1);
% lmiterm([3 1 1 0],1);
% 
% lmisys=getlmis;

% [tmin,xfeas]=feasp(lmisys)

