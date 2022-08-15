P=KeyboardInterrupt
O=float
E=True
C=property
import socket as B,time
from collections import namedtuple as D
from functools import partial as F
from six.moves import zip_longest as G
from six import print_ as H
from timeit import default_timer as A
from prettytable import PrettyTable as I
J=D('Statistics',['host','port','successed','failed','success_rate','minimum','maximum','average'])
Q=F(H,flush=E)
def K(x):return sum(x)/O(len(x))
class L:
	def __init__(C,family,type_,timeout):A=B.socket(family,type_);A.settimeout(timeout);C._s=A
	def connect(A,host,port=80):A._s.connect((host,int(port)))
	def shutdown(A):A._s.shutdown(B.SHUT_RD)
	def close(A):A._s.close()
class M:
	def __init__(A):A.table_field_names=[];A.rows=[]
	@C
	def raw(self):
		B=[]
		for A in self.rows:C=A.successed+A.failed;D='\n--- {}[:{}] tcping statistics ---'.format(A.host,A.port);E='\n{} connections, {} successed, {} failed, {} success rate'.format(C,A.successed,A.failed,A.success_rate);F='\nminimum = {}, maximum = {}, average = {}'.format(A.minimum,A.maximum,A.average);G=D+E+F;B.append(G)
		return ''.join(B)
	@C
	def table(self):
		A=I();A.field_names=self.table_field_names
		for B in self.rows:A.add_row(B)
		return'\n'+A.get_string()
	def set_table_field_names(A,field_names):A.table_field_names=field_names
	def add_statistics(A,row):A.rows.append(row)
class N:
	def __init__(A):A._start=0;A._stop=0
	def start(B):B._start=A()
	def stop(B):B._stop=A()
	def cost(A,funcs,args):
		A.start()
		for (B,C) in G(funcs,args):
			if C:B(*C)
			else:B()
		A.stop();return A._stop-A._start
class R:
	def __init__(A,host,port=80,timeout=1):A.print_=M();A.timer=N();A._successed=0;A._failed=0;A._conn_times=[];A._host=host;A._port=port;A._timeout=timeout;A.print_.set_table_field_names(['Host','Port','Successed','Failed','Success Rate','Minimum','Maximum','Average'])
	def _create_socket(A,family,type_):return L(family,type_,A._timeout)
	def _success_rate(B):
		C=B._successed+B._failed
		try:A=O(B._successed)/C*100;A='{0:.2f}'.format(A)
		except ZeroDivisionError:A='0.00'
		return A
	def statistics(A,n):C='{0:.2f}ms';B=A._conn_times if A._conn_times!=[]else[0];D=C.format(min(B));E=C.format(max(B));F=C.format(K(B));G=A._success_rate()+'%';A.print_.add_statistics(J(A._host,A._port,A._successed,A._failed,G,D,E,F))
	@C
	def result(self):return self.print_
	def ping(A,count=10):
		C=False
		for F in range(1,count+1):
			D=A._create_socket(B.AF_INET,B.SOCK_STREAM)
			try:time.sleep(1);G=A.timer.cost((D.connect,D.shutdown),((A._host,A._port),None));H=1000*G;C=E;A._conn_times.append(H)
			except B.timeout:C=E;A._failed+=1
			except P:A.statistics(F-1);raise P()
			else:A._successed+=1
			finally:D.close()
		return C