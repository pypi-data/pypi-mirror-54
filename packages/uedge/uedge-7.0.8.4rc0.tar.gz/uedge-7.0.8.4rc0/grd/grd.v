grd
# This is the 2-d grid construction package that adds orthogonal surfaces
# to the flux surfaces generated by the flx package.  This forms the basic
# structure for the plasma zone grid in the DEGAS code.
{
NIX = 3         # maximum number of coincident angle surfaces at x-point
MSEG = 15       # maximum number of segments on a flux curve
NALPHA = 4      # number of rotated coordinate systems used for spline fits
NDAT = 7        # dimensioning parameter for x-mesh data
NDATP2 = NDAT+2
}

***** Dimensions:
# dimensioning parameters - some from flx package
idim    integer
	# maximum number of angle coordinate surfaces
nix     integer /NIX/
	# number of coincident angle surfaces at x-point
mseg    integer /MSEG/
	# maximum number of segments on a flux curve
nalpha  integer /NALPHA/
	# number of rotated coordinate systems used for spline fits
nxuse(1:2)	integer
	# number of finite-size cells along core boundary = nxcore-1 for
	# double-null and limiter configurations
nptmp	integer	/300/
	# length of temporary arrays for upstream and plate surfaces in
	# S.R. meshmod
ndata		integer
	# data array length for SLATEC spline routine FC
nbkpt		integer
	# breakpoint array length for SLATEC spline routine FC
nconst		integer	/0/
	# constraint array length for SLATEC spline routine FC
integer nwdim	integer
	# workspace array length for SLATEC spline routine FC
integer niwdim	integer
	# workspace array length for SLATEC spline routine FC

***** Analgrd:
# common block with parameters for cylindrical & rectangular (IDEAL) grid
radm    real [m] /-1.e-4/   #minimum "radius" of cylinder or slab
radx    real [m]  /0.04/    #maximum "radius" of cylinder or slab
rad0    real [m]   /0./     #location of "radial" separ'x for cylinder or slab
rscalcore real [ ] /1./     #scale fac to change radial dimen. of core region
za0     real [m]   /0./     #position of left-hand axial boundary position
zax     real [m]   /1./     #position of right-hand axial boundary position
zaxpt   real [m]   /.75/    #position of x-point; uniform grid to here
tiltang real [deg] /0./     #inc. tilt angle of the divertor plate from 90 deg.
ixsnog  integer    /1/	    #poloidal ix where nonorthogonal mesh begins
zxpt_reset real [m] /0./    #reset x-pt2 here if >0 for single-region mesh
alfyt   real      /-2./     #exponent coeff. for y (radial) grid nonuiformity
tnoty   real      /0./      #shift if r(t)~del_r*tanh radial mesh profile
sratiopf real      /0./     #ratio of effec. alfyt in priv. flux region; calc
                            #internally to give same expans. rate if =0.
alfxt   real      /4.0/     #exponent coeff. for x (axial) grid nonuiformity
isadjalfxt integer /0/      #=1 changes alfxt slightly for smooth dx at ixpt2 
tctr    real      /0./      #relative location of dx maximum;0, left; 1., right
bpolfix real [T]   /.3/     #poloidal B-field for cartesian grid
btfix   real [T]   /5./     #total B-field for cartesian grid 
isgdistort integer /0/      #switch to distort poloidal grid
agsindx real       /0./     #max amplitude shift of poloidal cell face linear
 			    #linear in radial index iy
agsrsp  real       /0./     #max amplitude shift of poloidal cell face linear
                            #in real space - use either asgindx or asgrsp/not b
iynod   integer    /0/      #iy about which asgindx distortion is centered
rnod    real       /0./     #value of y about which asgrsp distortion centered
ixdstar integer    /1/      #ix where poloidal distortion begins

***** Torannulus:
acore	real [m]   /0.5/    #minor radius of core-edge bdry for mhdgeo=2
rm0	real [m]   /2./     #major radius of annulus for mhdgeo=2
edgewid real [m]   /0.1/    #width of simulated edge region for mhdgeo=2
dthlim  real [rad] /1e-4/   #polodial angular width of limiter cell
bpol0   real [T]   /0.2/    #poloidal B-field for mhdgeo=2 (annulus)
btor0   real [T]   /2./     #toroidal B-field for mhdgeo=2 on axis
radf(0:nym+1,0:4) _real [m] # minor radius of cells for mhdgeo=2
thpf(1:nxm,0:4)   _real [m] # poloidal angle of cells for mhdgeo=2
ibpmodel integer   /0/      #=0, Bpol=bpol0; =1, Bpol=bpol0*rm0/R
 
***** Magmirror:
zu(1:nxm,1:nym,0:4)   _real [m] #axial postions of vertices & center (0)
ru(1:nxm,1:nym,0:4)   _real [m] #radial postions of vertices & center (0)
bzu(1:nxm,1:nym,0:4)  _real [T] #axial B-field at vertices & center (0)
bru(1:nxm,1:nym,0:4)  _real [T] #radial B-field at vertices & center (0)
bmag(1:nxm,1:nym,0:4) _real [T] #total B-field at vertices & center (0)
nzc                 integer     #number of mesh pts along B-field
nrc                 integer     #number of radial mesh pts

***** Curves:
# common block from original grid code
xcurveg(npts,jdim)      _real	[m]
	# xcurve(n,j) is radial coordinate of nth data point on jth flux
	# contour
ycurveg(npts,jdim)      _real	[m]
	# ycurve(n,j) is vertical coordinate of nth data point on jth flux
	# contour
npointg(jdim)    _integer
	# npoint(j) is the number of data points on the jth flux contour
xxpoint         real	[m]
	# radial position of the (lower) x-point
yxpoint         real	[m]
	# vertical position of the (lower) x-point
rtanpl          real    [m]
	# radial position of "tangent point" (Bz = 0) on divertor plate
ztanpl          real    [m]
	# vertical position of "tangent point" (Bz = 0) on divertor plate

***** Linkco:
# common block from original grid code
cmeshx(idim,jdim)       _real	[m]
	# radial coordinates of PLANET/DEGAS mesh
cmeshy(idim,jdim)       _real	[m]
	# vertical coordinates of PLANET/DEGAS mesh
ixpoint(1:3,1:2)     integer
	# vertical indicies of x-point surfaces, for inboard and outboard
	# regions
yextend   real   [m]	/0./
	# fictitious lower boundary for constructing a mesh which extends
	# below the EFIT mesh boundary
dsmin           real    [m]	/0./
	# minimum separation of data points on flux contours
dsminx          real    [m]
	# minimum separation of data points from true x-point
dyjump  	real    [m]
	# a "jump" in a flux contour occurs when dy > dyjump for consecutive
	# points on the contour
alpha1          real    [degrees]	/45.0/
	# half-width angle that defines (up,down,left,right) directions
ityp(6,2)	integer	 /0,0,0,1,1,2,1,1,2,0,0,0/
	# flag for subroutine orthogx
	#	ityp = 0 --> search over 1 < i < npoint
	#	ityp = 1 --> search over 1 < i < ijump
	#	ityp = 2 --> search over ijump+1 < i < npoint
dxleft	real	[m]	/0./
	# radial step size for extrapolating flux contours
ndxleft	integer		/0/
	# incremental number of data points for extrapolating flux contours

***** Transfm:
# common block from original grid code
isegment(npts,jdim)      _integer
	# data point n belongs to spline segment number isegment(n,j) of
	# contour j
isys(mseg,jdim)         _integer
	# spline segment k of contour j uses coordinate system isys(k,j)
	# where isys=1  ---->   curve goes right, no rotation
	#       isys=2  ---->   curve goes up, rotate by pi/2
	#       isys=3  ---->   curve goes left, rotate by pi
	#       isys=4  ---->   curve goes down, rotate by 3*pi/2
alphasys(nalpha)        _real
	# rotation angle of the nth fixed, rotated coordinate system
ijump(jdim)     _integer
	# The discontinuity in flux contour occurs between data points
	# i=ijump and i=ijump+1

***** Spline:
# common block from original grid code
splcoef(npts,mseg,jdim)        _real
	# comment needed
xknts(npts,mseg,jdim)          _real
	# comment needed
ncap7(mseg,jdim)        _integer
	# comment needed

***** Argfc:
# argument list for SLATEC spline routine FC
xdatag(npts)	_real
# data array for independent variable x in SLATEC spline routine FC
ydatag(npts)	_real
# data array for dependent variable y in SLATEC spline routine FC
sddata(npts)	_real
# standard deviation array for data points in SLATEC spline routine FC
nord		integer	/4/
# order of spline fit (=4 for cubic splines)
bkpt(npts)	_real
# breakpoint array in SLATEC spline routine FC
xconst(nconst)	_real
# x data for constraints in SLATEC spline routine FC
yconst(nconst)	_real
# y data for constraints in SLATEC spline routine FC
nderiv(nconst)	_integer
# identifies type of constraints in SLATEC spline routine FC
mode		integer
# input/output flag for SLATEC spline routine FC
coeff(npts)	_real
# B-spline coefficients from SLATEC spline routine FC
wsla(nwdim)	_real
# real workspace for SLATEC spline routine FC
iwsla(niwdim)	_integer
# integer workspace for SLATEC spline routine FC

***** Inmesh:
# input data from user
isspnew		integer		/0/
	# flag for source of strike-point data
	# isspnew = 0 --> strike point data from eqdsk files
	#         = 1 --> user-specified values (rstrike(1:2),zstrike(1:2))
rstrike(1:2)	real	[m]
	# radial position of inboard:outboard strike point
zstrike(1:2)	real	[m]
	# vertical position of inboard:outboard strike point
istpnew		integer		/0/
	# flag for source of first-seed-point data (top of mesh)
	# istpnew = 0 --> 1st seed point at midplane for "dnbot"
	#         = 1 --> user-specified values (rtpnew(1:2),ztpnew(1:2))
rtpnew(1:2)	real	[m]
	# radial position of first inboard:outboard seed point
ztpnew(1:2)	real	[m]
	# vertical position of first inboard:outboard seed point
istptest(1:2)	     integer	/2*0/
	# flag for algorithm that defines top-of-mesh on inboard, (1), 
	# and outboard, (2), separatrix flux contours:
	# = 0  -->  test on R only
	# = 1  -->  test on R and Z
	# = 2  -->  test on Z only
ilmax(1:2)	integer
	# index of last angle surface ( at divertor plate ) in each region
seedxp(idim,noregs)     _real
	# normalized distance along core segment of separatrix
	# measured from first seed point (=0.) to x-point (=100.)
seedxpxl(idim,noregs)   _real
	# normalized distance along divertor leg of separatrix measured from
	# x-point (=0.) to last seed point (=100.) 
seed(idim,noregs)	_real
	# absolute distance along separatrix, measured from top of region,
	# to each angle-like mesh point
dissep(npts,noregs)	_real
	# absolute distance along separatrix, measured from top of region,
	# to each separatrix-flux-surface data point
distxp(noregs)		_real
	# absolute distance along core segment of separatrix
	# from first seed point to x-point
distxpxl(noregs)	_real
	# absolute distance along divertor leg of separatrix
	# from last seed point to x-point
x0g(noregs)      _real    [m]
	# major radius of the first seed point on the separatrix
xlast(noregs)      _real    [m]
	# major radius of the last seed point on the separatrix
y0g(noregs)      _real
	# vertical position of the first seed point on the separatrix
ylast(noregs)      _real
	# vertical position of the last seed point on the separatrix
isztest(1:2)	     integer	/2*0/
	# flag for algorithm that defines end-of-mesh on inboard, (1), 
	# and outboard, (2), separatrix flux contours:
	# = 0  -->  test on R only
	# = 1  -->  test on R and Z
	# = 2  -->  test on Z only
epslon_lim	real  /1.e-3/
	# ratio of limiter guard-cell x-width to adjacent cell
dalpha       real /5./
        # fuzziness or overlap (in degrees) of angle limits associ. with alpha1

***** Transit:
# common block from original grid code
xtrans(npts)  _real
	# x-position of data point for least-squares spline fit in rotated
	# system
ytrans(npts)  _real
	# y-position of data point for least-squares spline fit in rotated
	# system
wg(npts)          _real
	# weight of data point for least-squares spline fit in rotated
	# system

***** System:
# cliche from original grid code
istartg(mseg,jdim)       _integer
	# istart(k,j) is the i-index of the first data point on spline-fit
	# segment k of contour j, including any "extra" data points.
iendg(mseg,jdim)         _integer
	# iend(k,j) is the i-index of the last data point on spline-fit
	# segment k of contour j, including any "extra" data points.
m(mseg,jdim)            _integer
	# m(k,j) is the total number of data points for spline-fit segment k
	# of contour j, including any "extra" data points.
nseg(jdim)      _integer
	# comment needed
ixpointc(1:3,1:2)    integer
	# the i-index of x-point data in (xcurve,ycurve) arrays; j-index is
	# jsptrx.
xwork(npts)      _real
	# work array used in subroutine prune
ywork(npts)      _real
	# work array used in subroutine prune
istartc(noregs)  _integer
	# work array used in subroutine sow
iendc(noregs)    _integer
	# work array used in subroutine sow

***** UEgrid:
# input/output data for defining the grid in the UEDGE code
ixtop   integer
	# ix index of top "angle" surface opposite the x-point

***** Mmod:
# parameters that determine non-orthogonal mesh modifications
# Note: parameter ismmon has been moved to group Share of the com package
cmeshx0(idim,jdim)       _real	[m]
	# working copy of orthogonal mesh, used by meshmod3 (for ismmon=3)
cmeshy0(idim,jdim)       _real	[m]
	# working copy of orthogonal mesh, used by meshmod3 (for ismmon=3)
dsc(npts)	_real
	# temporary array for subroutine meshmod
	# distance (along x,ycurve) downstream from top-of-mesh 
	# to each flux surface data point
xcrv(npts)           _real
	# temporary array for x-coordinates in subroutine meshmod
ycrv(npts)           _real
	# temporary array for y-coordinates in subroutine meshmod
dsm(idim)	_real
	# distance (along cmeshx,y) downstream from top-of-mesh
dss(idim)	_real
	# distance (along separatrix cmeshx,y) downstream from top-of-mesh
dssleg(idim)	_real
	# distance (along separatrix cmeshx,y) downstream from x-point
dsmesh(idim)	_real
	# temporary array for subroutine meshmod; distance (along x,ycurve)
	# downstream from top-of-mesh to meshpoints
dsmesh0(idim)	_real
	# temporary array for subroutine meshmod
	# distance from top-of-mesh to meshpoints for ismmon=0 option
dsmesh1(idim)	_real
	# temporary array for subroutine meshmod
	# distance from top-of-mesh to meshpoints for ismmon=1 option
dsmesh2(idim)	_real
	# temporary array for subroutine meshmod
	# distance from top-of-mesh to meshpoints for ismmon=2 option
xmsh(idim)           _real
	# temporary array for x-coordinates in subroutine meshmod
ymsh(idim)           _real
	# temporary array for y-coordinates in subroutine meshmod
ntop1	integer
	# number of data points on the inboard top-of-mesh reference surface
rtop1(ntop1)	_real	[m]
	# radial position of data points on the inboard top-of-mesh
	# reference surface
ztop1(ntop1)	_real	[m]
	# vertical position of data points on the inboard top-of-mesh
	# reference surface
ntop2	integer
	# number of data points on the outboard top-of-mesh reference
	# surface
rtop2(ntop2)	_real	[m]
	# radial position of data points on the outboard top-of-mesh
	# reference surface
ztop2(ntop2)	_real	[m]
	# vertical position of data points on the outboard top-of-mesh
	# reference surface
istream			integer	/0/
	# option parameter for defining fixed upstream reference surface
	# istream=0	midplane+cut(ismmon=1) or top-of-mesh(ismmon=2)
	# istream=1	user-defined upstream surface arrays
isupstreamx			integer	/0/
	# option parameter for defining fixed upstream reference surface
	# isupstreamx=0	midplane+cut(ismmon=1) or top-of-mesh(ismmon=2)
	# isupstreamx=1	orthogonal surface (SOL and PF) through x-point
nupstream1	integer
	# number of data points on the inboard upstream reference surface
rupstream1(nupstream1)	_real	[m]
	# radial position of data points on the inboard upstream reference
	# surface
zupstream1(nupstream1)	_real	[m]
	# vertical position of data points on the inboard upstream reference
	# surface
nupstream2	integer
	# number of data points on the outboard upstream reference surface
rupstream2(nupstream2)	_real	[m]
	# radial position of data points on the outboard upstream reference
	# surface
zupstream2(nupstream2)	_real	[m]
	# vertical position of data points on the outboard upstream
	# reference surface
ndnstream1	integer
	# number of data points on the inboard downstream reference surface
rdnstream1(ndnstream1)	_real	[m]
	# radial position of data points on the inboard downstream reference
	# surface
zdnstream1(ndnstream1)	_real	[m]
	# vertical position of data points on the inboard downstream
	# reference surface
ndnstream2	integer
	# number of data points on the outboard downstream reference surface
rdnstream2(ndnstream2)	_real	[m]
	# radial position of data points on the outboard downstream
	# reference surface
zdnstream2(ndnstream2)	_real	[m]
	# vertical position of data points on the outboard downstream
	# reference surface
iplate			integer	/0/
	# option parameter for defining divertor plates
	# iplate=0	orthogonal plates
	# iplate=1	user-defined divertor plates
nplate1	integer
	# number of data points on the inboard divertor plate surface
rplate1(nplate1)	_real	[m]
	# radial position of data points on the inboard divertor plate surface
zplate1(nplate1)	_real	[m]
	# vertical position of data points on the inboard divertor plate
	# surface
nplate2	integer
	# number of data points on the outboard divertor plate surface
rplate2(nplate2)	_real	[m]
	# radial position of data points on the outboard divertor plate
	# surface
zplate2(nplate2)	_real	[m]
	# vertical position of data points on the outboard divertor plate
	# surface
ntop		integer
	# temporary variable for subroutine meshmod
rtop(nptmp)	_real	[m]
	# temporary array for subroutine meshmod
ztop(nptmp)	_real	[m]
	# temporary array for subroutine meshmod
ntop0		integer
	# temporary variable for subroutine meshlim
rtop0(nptmp)	_real	[m]
	# temporary array for subroutine meshlim
ztop0(nptmp)	_real	[m]
	# temporary array for subroutine meshlim
nbot		integer
	# temporary variable for subroutine meshlim
rbot(nptmp)	_real	[m]
	# temporary array for subroutine meshlim
zbot(nptmp)	_real	[m]
	# temporary array for subroutine meshlim
nupstream		integer
	# temporary variable for subroutine meshmod
rupstream(nptmp)	_real	[m]
	# temporary array for subroutine meshmod
zupstream(nptmp)	_real	[m]
	# temporary array for subroutine meshmod
ndnstream		integer
	# temporary variable for subroutine meshmod
rdnstream(nptmp)	_real	[m]
	# temporary array for subroutine meshmod
zdnstream(nptmp)	_real	[m]
	# temporary array for subroutine meshmod
nplate		integer
	# temporary variable for subroutine meshmod
rplate(nptmp)		_real	[m]
	# temporary array for subroutine meshmod
zplate(nptmp)		_real	[m]
	# temporary array for subroutine meshmod
nplate0		integer
	# temporary variable for subroutine meshmod
rplate0(nptmp)		_real	[m]
	# temporary array for subroutine meshmod
zplate0(nptmp)		_real	[m]
	# temporary array for subroutine meshmod
dsnorm(idim)		_real
	# temporary array for subroutine meshmod2
wtold	real	/0.5/
	# weight factor for spatial smoothing of angle-like mesh surfaces
	# wtold=1.0 ==> no smoothing
	# wtold=0.5 ==> (1,2,1) relative weighting of (j-1,j,j+1)
	# wtold=0.0 ==> (1,0,1) relative weighting of (j-1,j,j+1)
nsmooth	integer	/2/
	# number of times to apply the smoothing algorithm to each
	# angle-like surface after non-orthogonal plate construction
fuzzm	real	[m]	/1.0e-08/
	# a measure of the "fuzziness" in meshpoint coordinates  
delmax	real	[m]	/1.0e-08/
	# estimated maximum deviation of mesh points from exact flux
	# surfaces (used only in subroutine smooth)
wtmesh1	real	/0.5/
	# weight factor for combining ismmon=1 and ismmon=2 meshes
	# wtmesh1=1 ---> same as ismmon=1
	# wtmesh1=0 ---> same as ismmon=2
wtm1(idim)	_real
	# temporary array of weight factors for merging limiter mesh
	# with original (unmodified) mesh
dmix0	real	/0./
	# normalized poloidal mixing length for combining mesh0 with mesh12
	# =0. --> abrupt  change from orthogonal mesh to mesh12 at upstream 
        #         position
	# =1. --> gradual change from orthogonal mesh to mesh12 between 
        #         upstream and downstream positions
cmeshx3(idim,jdim)       _real	[m]
	# reference mesh for flamefront modifications
cmeshy3(idim,jdim)       _real	[m]
	# reference mesh for flamefront modifications
nff1	integer
	# number of data points on the inboard flamefront
rff1(nff1)	_real	[m]
	# radial position of data points on the inboard flamefront
zff1(nff1)	_real	[m]
	# vertical position of data points on the inboard flamefront
nff2	integer
	# number of data points on the outboard flamefront
rff2(nff2)	_real	[m]
	# radial position of data points on the outboard flamefront
zff2(nff2)	_real	[m]
	# vertical position of data points on the outboard flamefront
nff		integer
	# temporary variable for subroutine meshff
rff(nptmp)	_real	[m]
	# temporary array for subroutine meshff
zff(nptmp)	_real	[m]
	# temporary array for subroutine meshff
dsmesh3(idim)	_real
	# temporary array for subroutine meshff
	# distance from top-of-mesh to original meshpoints (no flamefront)
dsmeshff(idim)	_real
	# temporary array for subroutine meshff
	# distance from top-of-mesh to modified meshpoints (flamefront)
cwtffu		real	/1./
	# exponent for weight function variation between x-point and flamefront
	# wt(ix)=wtff*fac(ix)**cwtff where fac(ix) varies linearly from
	# zero at xpoint to unity at flamefront.
cwtffd		real	/1./
	# exponent for weight function variation between flamefront and plate
	# wt(ix)=wtff*fac(ix)**cwtff where fac(ix) varies linearly from
	# zero at plate to unity at flamefront.
isxtform	integer	/1/
	# flag for choosing various forms of x(ix) near flamefront
	# =1 --> specify slope factor at flamefront only (default)
	# =2 --> specify slope factor at flamefront and upstream
	# =3 --> specify slope factor at flamefront, upstream and downstream
iswtform	integer /0/
	# flag for choosing various forms of weight factors near flamefront
	# =0 --> wt(ix)=wtff for all ix (default)
	# =1 --> wt(ix)~wtff*abs(ix-ixlimit)**cwtff between flamefront and
	#        limiting surface at xpoint (upstream) or plate (downstream).
wtff1		real
	# maximum weight factor for combining meshes w and w/o flamefront
	# wtff=1 ---> full flamefront mesh
	# wtff=0 ---> no flamefront modifications
slpxff1		real
	# slope factor at flamefront position
	# slpxff < 1  makes mesh finer at flamefront
	# slpxff > 1  makes mesh coarser at flamefront
slpxffu1	real
	# slope factor at upstream limit (x-point) of flamefront mesh
	# slpxuu < 1  makes mesh finer
	# slpxuu > 1  makes mesh coarser
slpxffd1	real
	# slope factor at downstream limit (plate) of flamefront mesh
	# slpxuu < 1  makes mesh finer
	# slpxuu > 1  makes mesh coarser
nxdff1		integer		/0/
	# number of cells between flame front and divertor plate
	# on inner leg (region 1)
wtff2		real
	# maximum weight factor for combining meshes w and w/o flamefront
	# wtff=1 ---> full flamefront mesh
	# wtff=0 ---> no flamefront modifications
slpxff2		real
	# slope reduction factor for flamefront mesh
	# slpxff < 1  makes mesh finer at flamefront
	# slpxff > 1  makes mesh coarser at flamefront
slpxffu2	real
	# slope factor at upstream limit (x-point) of flamefront mesh
	# slpxuu < 1  makes mesh finer
	# slpxuu > 1  makes mesh coarser
slpxffd2	real
	# slope factor at downstream limit (plate) of flamefront mesh
	# slpxuu < 1  makes mesh finer
	# slpxuu > 1  makes mesh coarser
nxdff2		integer		/0/
	# number of cells between flame front and divertor plate
	# on outer leg (region 2)

***** Refinex:
# data used for mesh refinement near the x-point
isrefxptn	integer	/1/
	# flag for choosing x-point mesh refinement algorithm
	# =0  old interpolation method
	# =1  new flux-surface-based method
nxmod	integer	/2/
	# number of 'upstream' poloidal cells (per quadrant) in the
	# original mesh that we modify by calling subroutine refinex
alfxptl real /1./	# use as alfxpt for cells below(l) the x-pt;
        # frac=(i/(nxxpt+nxmod))**alfxpt for extra x-pt grid spacing below x-pt
alfxpt2l real /1./	# use as alfxpt2 for cells below(l) the x-pt;
        # frac2=(i/(nxxpt+nxmod-1))**alfxpt2 for mixing fixed lngth & 
	# flux-surface length in adding extra x-pt cells below x-pt
alfxptu real /1./	# use as alfxpt for cells above(u) the x-pt;	
        # frac=(i/(nxxpt+nxmod))**alfxpt for extra x-pt grid spacing above x-pt
alfxpt2u real /1./	# use as alfxpt2 for cells above(u) the x-pt;	
        # frac2=(i/(nxxpt+nxmod-1))**alfxpt2 for mixing fixed lngth & 
	# flux-surface length in adding extra x-pt cells above x-pt
alfxpt  real /1./	# work var for alfxptl,u for below(l)/above(u) x-pt
        # frac=(i/(nxxpt+nxmod))**alfxpt for setting extra x-pt grid spacing
alfxpt2 real /1./	# work var for alfxptsl,u for below(l)/above(u) x-pt
        # frac2=(i/(nxxpt+nxmod-1))**alfxpt2 for mixing fixed lngth & 
	# flux-surface length in adding extra x-pt cells
rsu(0:nym+2)	_real	[m]
	# working array (for each quadrant) that contains r-coord's of
	# upstream reference surface
zsu(0:nym+2)	_real	[m]
	# working array (for each quadrant) that contains z-coord's of
	# upstream reference surface
rsx(0:nym+2)	_real	[m]
	# working array (for each quadrant) that contains r-coord's of
	# reference surface passing thru the x-point
zsx(0:nym+2)	_real	[m]
	# working array (for each quadrant) that contains z-coord's of
	# reference surface passing thru the x-point
nflux	integer
	# number of data points in the working arrays rflux & zflux
rflux(npts)	_real	[m]
	# working array that contains r-coord's of flux surface data points
zflux(npts)	_real	[m]
	# working array that contains z-coord's of flux surface data points
dsflux(npts)	_real	[m]
	# working array that contains cumulative distance from upstream
	# reference surface
rmm(0:nym,0:nxm)	_real	[m]
	# working array that contains r-coord's of angle-like surfaces
	# in refined region near x-point
zmm(0:nym,0:nxm)	_real	[m]
	# working array that contains z-coord's of angle-like surfaces
	# in refined region near x-point
nsmoothx	integer	/8/
	# number of times to apply the smoothing algorithm to each
	# angle-like surface after mesh refinement near the x-point

***** Xmesh:
# data for analytic definition of xfcn(t) on separatrix
ndat    integer         /NDAT/
	# number of data values for xfcn(t)
xdat(ndat) 	_real	[m]
	# data values for xfcn
tdat(ndat) 	_real
	# data values for t
kxmesh  integer /1/
	# switch parameter for choosing model that defines x-mesh :
	#       kxmesh=0        use old model (manual def. of seed points)
	#       kxmesh=1        use linear*rational form for x(t)
	#       kxmesh=2        use linear*exponential form for x(t)
	#       kxmesh=3        use spline form for x(t)
	#       kxmesh=4        use exponential+spline form for x(t)
slpxt	real	/1.0/
	# slope enhancement factor for x(t) near the "top" of the core
	# plasma
alfx(2)		real	/2*0.1/
	# log( dx(n+1)/dx(n) ) for 'gas' cells near the divertor plates
dxgas(2)	real	[m]
	# poloidal size of first 'gas' cell at inboard and outboard plates
nxgas(2)	integer
	# number of poloidal 'gas' cells at inboard and outboard plates
dt1	real
	# normalized-index distance (t) from inboard plate to 'extra' data
	# point
dx1	real	[m]
	# physical distance (x) from inboard plate to 'extra' data point
dt2	real
	# normalized-index distance (t) from outboard plate to 'extra' data
	# point
dx2	real	[m]
	# physical distance (x) from outboard plate to 'extra' data point
ileft	integer	/0/
	# type of end condition at the left endpoint
	#     = 1  first derivative specified by dleft
	#     = 2  second derivative specified by dleft
dleft	real	/0.0/	[m]
	# derivative at left endpoint
iright	integer	/0/
	# type of end condition at the right endpoint
	#     = 1  first derivative specified by dright
	#     = 2  second derivative specified by dright
dright	real	/0.0/	[m]
	# derivative at right endpoint
kord	integer	/4/	# order of spline (=4 for cubic interpolation)
ndatp2	integer	/NDATP2/ 	# NDATP2 = NDAT+2
kntopt	integer	/1/		# knot selection option flag
tknt(ndatp2+4)	_real		# knot locations
z1work(5*(ndat+2))	_real	# work array for BINT4 spline construction
z1cscoef(ndatp2)	_real	# spline coefficients
wrk1(3*kord)		_real	# work array for B1VAL spline evaluation
iflag1			integer	# output status flag from B1VAL

***** Dnull_temp:
	# temporary storage for upper and bottom halves of double-null mesh
nxmb		integer	# number of cells in poloidal direction
nymb		integer	# number of cells in radial direction
rmb(0:nxmb+1,0:nymb+1,0:4)     _real [m]    # radial cell position
zmb(0:nxmb+1,0:nymb+1,0:4)     _real [m]    # vertical cell position
ixpt1b		integer	# poloidal index of cells at x-point on inboard side
ixtopb		integer	# poloidal index of cells at top of mesh
ixpt2b		integer	# poloidal index of cells at x-point on outboard side
iysptrxb	integer	# radial index of cells just inside the separatrix
nxmu		integer	# number of cells in poloidal direction
nymu		integer	# number of cells in radial direction
rmu(0:nxmu+1,0:nymu+1,0:4)     _real [m]    # radial cell position
zmu(0:nxmu+1,0:nymu+1,0:4)     _real [m]    # vertical cell position
ixpt1u		integer	# poloidal index of cells at x-point on inboard side
ixtopu		integer	# poloidal index of cells at top of mesh
ixpt2u		integer	# poloidal index of cells at x-point on outboard side
iysptrxu	integer	# radial index of cells just inside the separatrix

***** Expseed:
        # variables to control exponential poloidal mesh in sub exponseed
fraclplt(2)   real  /.6,.6/     #frac of divertor leg with near-plate spacing
alfxdiv(2)    real /.18,.18/    #exponential factor for cell-size expansion
alfxcore(2)   real  /.4,.4/     #exponential factor for cell-size expansion
shift_seed_leg(2)  real /0.,0./ #shift in seed away from Xpt toward plate
shift_seed_core(2) real /1.,1./ #shift in seed away from Xpt toward top
nxlplt(2)   integer     /12,12/ #num poloidal cells in leg-plate region
nxlxpt(2)   integer     /4,4/   #num pol cells in leg-xpt region; 
			        #note nxlplt+nxlxpt = nxleg (must check)
fcorenunif  real        /0.8/   #frac pol core mesh with expon mesh

***** Xfcn:
	# contains various x-mesh functional forms
xfcn(t)  function
	# defines analytic x-mesh in terms of normalized cell index 0 < t <
	# 1.  the divertor leg distribution has a rational function form.
xfcn2(t)  function
	# defines analytic x-mesh in terms of normalized cell index 0 < t <
	# 1.  the divertor leg distribution has a linear*exponential
	# function form.
xfcn3(t)  function
	# defines x-mesh in terms of normalized cell index 0 < t < 1.  a
	# cubic spline connects points.
xfcn4(t,nxtotal)  function
	# defines x-mesh in terms of normalized cell index 0 < t < 1.  form
	# is exponential near plates and cubic spline for interior region
xcscoef	  subroutine
	# calls spline-fitting routine BINT4

***** Driver:
	# user-callable subroutines
setidim	subroutine
	# sets dimensions for angle-like arrays
grdrun	subroutine
	# main driver routine for grd package
ingrd	subroutine
	# sets input data for grd package
codsys(j,icood,iseg,is,dy,region:integer,alpha1)        subroutine
	# constructs segmented spline fits to a flux contour
findalph(nsys,iseg,j,xob,yob,alphab) subroutine
	# finds the rotation angle.
readflx         subroutine
	# read input data from flx package in file flx-grd.
prune           subroutine
	# inserts x-points on the separatrix contours, and removes
	# closely-spaced points on all contours.
extend          subroutine
	# extrapolates contours, if necessary, below the plate surface.
splfit          subroutine
 	# constructs segmented spline fits to flux contours using s.r. codsys
sow             subroutine
	# generates the seed points along the separatrix
meshgen(region:integer)         subroutine
	# generates a mesh by finding orthogonal curves to (xcurve,ycurve)
orthogx(ixtyp,i,j0,j,xob,yob,alphab)    subroutine
	# constructs the orthogonal point on j from the given x-point
	# coordinates (xob,yob); the search is limited to the
	# (upper,lower,entire) length of flux surface j by ixtyp=(1,2,0); On
	# output, alpha is the local rotation angle of the jth flux surface
	# at (xob,yob).  Note that (xob,yob) are used as both input and
	# output arguments.  (i,j0) are informational only.
orthogrd(ixtyp,i,j0,j,xob,yob,alphab)    subroutine
 	# constructs the orthogonal point on j from the given point (xob,yob)
	# on j0; the search is limited to the (upper,lower,entire) length of
	# flux surface j by ixtyp=(1,2,0); alpha is the local rotation angle
	# of the jth flux surface at (xob,yob).  Note that (xob,yob,alpha)
	# are used as both input and output arguments.  (i,j0) are
	# informational only.
readgrid(fname:string,runid:string)	subroutine
	# This subroutine reads a formatted data file of (R,Z) coordinates
	# and magnetic field data for the UEDGE code.
writesn(fname:string,runid:string)	subroutine
	# This subroutine converts (cmeshx,cmeshy) data into (rm,zm) data
	# and writes a formatted data file of (R,Z) coordinates
	# and magnetic field data for a single-null divertor configuration.
writedn(fname:string,runid:string)	subroutine
	# This subroutine converts (cmeshx,cmeshy) data into (rm,zm) data
	# and writes a formatted data file of (R,Z) coordinates
	# and magnetic field data for the outboard half of an up/down
	# symmetric double-null configuration.
writedata(fname:string,runid:string)	subroutine
	# This subroutine writes a formatted data file of (R,Z) coordinates
	# and magnetic field data for the UEDGE code.
writednf(fname:string,runid:string)	subroutine
	# This subroutine writes a formatted data file of (R,Z) coordinates
	# and magnetic field data for a full double-null geometry.
intersect2(x1:real,y1:real,i1min:integer,i1max:integer, \
           x2:real,y2:real,i2min:integer,i2max:integer, \
           xc:real,yc:real,i1c:integer,i2c:integer,	\
           fuzz:real,ierr:integer)	subroutine
	#     Find the intersection of the two segmented curves :
	#     (x1(i),y1(i)) i=i1min,i1max and (x2(i),y2(i)) i=i2min,i2max
	#     Return the intersection point (xc,yc) and the node indices i1c
	#     and i2c such that the intersection point lies between nodes
	#     i1c and i1c+1 of curve 1 and nodes ic2 and ic2+1 of curve 2.
	#     fuzz is the absolute uncertainty in the data point positions.
	#     Return error flag ierr=1 if no intersection is found.
meshmod2(region:integer)         subroutine
	# generates a modified mesh with the same normalized distribution of
	# points along every flux surface.
smooth(i:integer,j1:integer,j2:integer)	subroutine
	# smoothes spatial irregularities in angle-like surface (i) between
	# flux surfaces (j1) and (j2) ---> modified cmeshx,y
writeue		subroutine
	# convert from DEGAS-indexed (cmeshx,cmeshy) to UEDGE-indexed
	# (rm,zm) and write these into an ascii grid-data file, gridue.
grd2wdf		subroutine
	# write grid information for DEGAS namelist to unformatted file
	# grd-wdf
evalspln(iseg:integer,j:integer,xo:real,yo:real)	subroutine
	# evaluates the spline representation for the y-coordinate and its
	# derivatives (yo(1:4)) on a segment (iseg) of a flux surface (j) at
	# the input x-coordinate (xo), where (xo,yo) are in the
	# local/rotated coordinate system of the spline (see isys(iseg,j)
	# and the corresponding alphasys for the rotation angle)
idealgrd	subroutine
	# calculates either a cylindrical mesh for mhdgeo=0, or a cartesian
	# mesh for mhdgeo=-1
mirrorgrd	subroutine
	# calculates a R,Z values for a magnetic mirror read in via a PDB file
gett		subroutine
	# generates top-of-mesh reference surfaces for use by meshmod3
getu		subroutine
	# generates upstream reference surfaces for use by meshmod3
getd		subroutine
	# generates downstream reference surfaces for use by meshmod3
getp		subroutine
	# generates orthogonal plate reference surfaces for use by meshmod3
meshmod3(region:integer)	subroutine
	# generates a modified mesh as defined by parameters wtmesh1 and
	# dmix0, and by arrays for the plate and stream reference surfaces.
smoother	subroutine
	# applies smoothing algorithm to all angle-like flux surfaces in
	# the mesh; number of applications is controlled by nsmooth.
smoother2	subroutine
	# applies smoothing algorithm to all angle-like flux surfaces in
	# the outboard half of the mesh only
meshff(region:integer)		subroutine
	# generates a modified mesh with refinement near a flamefront
	# surface; degree of modification is controlled by wtff and slpxff.
	# flamefront surface is defined in arrays rff1,zff1,rff2,zff2.
fpoloidal(psi:real)	function
	# evaluates the MHD flux function F(psi) = R*B_toroidal for
	# arbitrary psi by interpolation on the array fpol(1:nxefit)
	# from the EFIT eqdsk file.
pressure(psi:real)	function
	# evaluates the MHD plasma pressure P(psi) for arbitrary psi by
	# interpolation on the array pres(1:nxefit) from the EFIT eqdsk file.
psif(r,z)	function
	# evaluates the EFIT 2-D spline for psi
brf(r,z)	function
	# evaluates the radial magnetic field from the 2-D spline for psi
bzf(r,z)	function
	# evaluates the vertical magnetic field from the 2-D spline for psi
rsurface(quadrant:integer)	subroutine
	# copies angle-like surface data to reference surface arrays
	# rsu,zsu,rsx,zsx for x-point mesh refinement
fluxcurve(quadrant:integer,iy:integer)	subroutine
	# copies flux surface data from (xcurveg,ycurveg) to the work
	# arrays (rflux,zflux) used for x-point mesh refinement
refinexm	subroutine
	# refine the mesh in the poloidal direction near the x-point
	# with parameters nxmod, nxxpt and alfxpt set by user
refine_xpt	subroutine
	# refine the mesh in the poloidal direction near the x-point
	# with parameters nxmod, nxxpt and alfxpt set by user
smoothx(rmm:real,zmm:real,nd1:integer,nd2:integer,\
               iy1:integer,iy2:integer,quadrant:integer)	subroutine
	# smooth spatial irregularities in the angle-like surface
	# defined by the arrays rmm(iy1:iy2) and zmm(iy1:iy2) while ensuring
	# that the smoothed points lie exactly on flux surfaces.
mapdnbot	subroutine
	# maps bottom-half mesh data (rmb,zmb) into mesh arrays (rm,zm)
	# for full double null and sets special mesh indices
mapdntop	subroutine
	# maps upper-half mesh data (rmu,zmu) into mesh arrays (rm,zm)
	# for full double null and sets special mesh indices
magnetics(ixmin,ixmax,iymin,iymax)	subroutine
	# evaluate magnetic field data for mesh cells (rm,zm) with
	# indices in the range ixmin<=ix<=ixmax and iymin<=iy<=iymax;
	# uses 2-d spline fit to eqdsk data
add_guardc_tp	subroutine
	# construct infinitesimal guard cells at target plates for full
	# double-null mesh
exponseed       subroutine
        # computes seeds point for poloidal mesh based on exponentals

