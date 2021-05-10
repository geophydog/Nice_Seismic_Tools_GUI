import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic

class ArrayAnalysisDemo:
    '''
    Demo of seismic array analysis.
    '''
    def __init__(self):
        self.x = np.array([-5.23409808, -2.37268882, 12.40721021, 4.81935806,
                           -14.87786286, 7.44097255, -5.42163854, -5.99693746])
        self.y = np.array([-2.32292146, 4.55091928, 3.64079618, 3.13253048,
                           -4.82245826, -12.79647225, -3.49166719, 19.42172091])

    def show_demo(self):
        x = self.x; y = self.y
        plt.figure(figsize=(18, 8))
        plt.subplot(121)
        n = len(x)
        for i in range(n - 1):
            for j in range(i + 1, n):
                plt.plot([x[i], x[j]], [y[i], y[j]], lw=1, color='#AAAAAA', zorder=0)
        plt.scatter(x, y, marker='v', s=300, facecolor='#87CEFA', edgecolor='k', lw=1, zorder=2)
        plt.scatter(0, 0, marker='v', s=500, facecolor='#FFC0CB', edgecolor='k', lw=1, zorder=3)
        plt.scatter(-40, -40, marker='*', s=1000, facecolor='#FFA500', edgecolor='k', lw=1, zorder=4)
        plt.scatter(15, 38, marker='v', s=200, facecolor='#87CEFA', edgecolor='k', lw=1)
        plt.scatter(15, 32, marker='v', s=200, facecolor='#FFC0CB', edgecolor='k', lw=1)
        plt.annotate('', xy=(20, 20), xytext=(0, 0),
                     arrowprops=dict(width=1.5, headwidth=10, headlength=20, color='k'), zorder=1)
        plt.annotate('', xy=(20, 0), xytext=(0, 0),
                     arrowprops=dict(width=1.5, headwidth=10, headlength=20, color='k'), zorder=1)
        plt.annotate('', xy=(0, 20), xytext=(0, 0),
                     arrowprops=dict(width=1.5, headwidth=10, headlength=20, color='k'), zorder=1)
        plt.plot([-40, 0], [-40, 0], ls='--', color='r', lw=2, zorder=0.5)
        plt.plot([20, 20], [0, 20], ls='--', color='k', lw=2, zorder=0.5)
        plt.plot([0, 20], [20, 20], ls='--', color='k', lw=2, zorder=0.5)
        plt.plot(12 * np.cos(np.linspace(np.pi / 4, np.pi / 2, 51)),
                 12 * np.sin(np.linspace(np.pi / 4, np.pi / 2, 51)), color='g', lw=2, zorder=1)
        plt.plot(10 * np.cos(np.linspace(-3 * np.pi / 4, np.pi / 2, 51)),
                 10 * np.sin(np.linspace(-3 * np.pi / 4, np.pi / 2, 51)), color='g', lw=2, zorder=1)
        plt.text(10, -10, r'$\theta$', fontdict={'size': 25})
        plt.text(4, 13, r'$\alpha$', fontdict={'size': 25})
        plt.text(22, 20, r'$\vec{s}$', fontdict={'size': 25})
        plt.text(-43, 38, r'$\vec{s}$: slowness vector', fontdict={'size': 15})
        plt.text(-43, 32, r'$\theta$: back-azimuth', fontdict={'size': 15})
        plt.text(-43, 26, r'$\alpha$: angle of slowness', fontdict={'size': 15})
        plt.text(20, -4, r'$s_x$', fontdict={'size': 25})
        plt.text(2, 22, r'$s_y$', fontdict={'size': 25})
        plt.text(-43, 20, r'$\theta=\alpha+\pi$', fontdict={'size': 15})
        plt.text(-35, -41.5, r'source', fontdict={'size': 25})
        plt.text(18, 37, ': station', fontdict={'size': 15})
        plt.text(18, 31, ': array center', fontdict={'size': 15})
        plt.text(-2, 45, r'N', fontdict={'size': 25, 'color': 'b'})
        plt.text(-1.5, -50, r'S', fontdict={'size': 25, 'color': 'b'})
        plt.text(46, -2, r'E', fontdict={'size': 25, 'color': 'b'})
        plt.text(-52, -2, r'W', fontdict={'size': 25, 'color': 'b'})
        plt.axhline(y=0, color='b', lw=2, zorder=1)
        plt.axvline(x=0, color='b', lw=2, zorder=1)
        plt.grid(ls=(10, (8, 5)), color='gray', lw=0.7, zorder=0)
        plt.axis('equal')
        plt.xlim(-45, 45)
        plt.ylim(-45, 45)
        plt.xticks(fontsize=0)
        plt.yticks(fontsize=0)

        plt.subplot(122)
        plt.text(-0.1, 0.73, r'CSDM', rotation=90,
                 fontdict={'size': 20})
        plt.text(0, 0.9,
                 r'$ARF(\theta, \vec{s}, f)=\frac{1}{N*(N-1)}\sum_{m=1}^{N-1}\sum_{n=m+1}^Ne^{-i2\pi f \vec{s} \cdot (\vec{r}_n-\vec{r}_m)}$',
                 fontdict={'size': 15})
        plt.text(0, 0.78,
                 r'$P(\theta, \vec{s}, f)=\frac{1}{M}\sum_{m=1}^{N-1}\sum_{n=m+1}^NC_{mn}(f)e^{-i2\pi f \vec{s} \cdot (\vec{r}_n-\vec{r}_m)}$',
                 fontdict={'size': 15})
        plt.text(0, 0.69, r'$C_{mn}(f)=\frac{U_m^*(f)U_n(f)}{\sqrt{|U_m(f)|^2+|U_n(f)|^2}}$',
                 fontdict={'size': 16})
        plt.text(0, 0.59, r'$\vec{s}=S[sin(\theta-\pi), cos(\theta-\pi)]^T$',
                 fontdict={'size': 20})
        plt.plot([-0.01, 0.92, 0.92, -0.01, -0.01], [0.54, 0.54, 1, 1, 0.54], color='gray', lw=1)

        plt.text(-0.1, 0.21, r'Relative', rotation=90,
                 fontdict={'size': 20})
        plt.text(0, 0.38,
                 r'$ARF(\theta, \vec{s}, f)=\frac{1}{N}\sum_{n=1}^Ne^{-i2\pi f \vec{s} \cdot (\vec{r}_n-\vec{r}_0)}$',
                 fontdict={'size': 17})
        plt.text(0, 0.28,
                 r'$P(\theta, \vec{s}, f)=\frac{1}{N}\sum_{n=1}^Ne^{-i2\pi f \vec{s} \cdot (\vec{r}_n-\vec{r}_0)}U_n(f)$',
                 fontdict={'size': 17})
        plt.text(0, 0.16, r'$\vec{r}_0=\frac{1}{N}\sum_{n=1}^N\vec{r}_n=\frac{1}{N}\sum_{n=1}^N[x_n, y_n]^T$',
                 fontdict={'size': 17})
        plt.plot([-0.01, 0.92, 0.92, -0.01, -0.01], [0.1, 0.1, 0.49, 0.49, 0.1], color='gray', lw=1)
        plt.xlim(-0.2, 1)
        plt.ylim(0.07, 1.03)
        plt.xticks([])
        plt.yticks([])
        plt.axis('equal')
        plt.show()

# Basic operations.
class BasicOperation:
    # The bearing (or azimuth) of the 2nd point relative to the 1st one.
    def azimuth(self, la1, lo1, la2, lo2):
        d2r = np.pi / 180.
        dlo = (lo2 - lo1) * d2r
        y = np.sin(dlo) * np.cos(la2 * d2r)
        x = np.cos(la1 * d2r) * np.sin(la2 * d2r) - np.sin(la1 * d2r) * np.cos(la2 * d2r) * np.cos(dlo)
        th = np.arctan2(y, x)
        az = (th / d2r + 360) % 360
        return az

    def new_xy(self, y1, x1, y2, x2):
        az = self.azimuth(y1, x1, y2, x2) * np.pi / 180
        dist = geodesic((y1, x1), (y2, x2), ellipsoid='WGS-84').km
        return np.array([np.sin(az), np.cos(az)])*dist

    def reference_position(self, xy, sys='degree'):
        pos = xy.copy()
        x0 = np.mean(xy[:, 0])
        y0 = np.mean(xy[:, 1])
        n = len(xy[:, 0])
        if sys == 'degree':
            for i in range(n):
                pos[i] = self.new_xy(y0, x0, xy[i, 1], xy[i, 0])
            return pos*1e3
        else:
            pos[:, 0] -= x0
            pos[:, 1] -= y0
            if sys == 'kilometer':
                return pos*1e3
            return pos

    def cross_position(self, xy, sys='degree'):
        n = len(xy[:, 0])
        m = (n-1) * n // 2
        pos = np.zeros((m, 2))
        index = 0
        if sys == 'degree':
            for i in range(n-1):
                for j in range(i+1, n):
                    pos[index] = self.new_xy(xy[i, 1], xy[i, 0], xy[j, 1], xy[j, 0])
                    index += 1
            return pos*1e3
        else:
            for i in range(n-1):
                for j in range(i+1, j):
                    pos[index] = np.array([xy[j, 0]-xy[i, 0], xy[j, 1]-xy[i, 1]])
                    index += 1
            if sys == 'kilometer':
                return pos*1e3
            return pos

    def relative_position(self, xy, ptype=0, sys='degree'):
        if ptype == 0:
            return self.reference_position(xy, sys=sys)
        return self.cross_position(xy, sys=sys)

    # Check the inout data types.
    def check_input(self, xy, sys):
        if type(xy) is not np.ndarray:
            print('The coordinates must be numpy.ndarray data of shape nx2!')
            exit(1)
        if not isinstance(sys, str):
            print('parameter sys should be string type!')
            exit(1)

# Array response (or transfer) function.
class ArrayResponse(BasicOperation):
    def __init__(self, xy, sys='degree'):
        super().check_input(xy, sys)
        self.sys = sys
        self.xy = xy

    def general_harmonic_response(self, f=0.05, s1=0, s2=1e-3, b1=0, b2=360,
                s0=0, b0=90, sn=51, bn=121, ptype=0):
        d2r = np.pi / 180.
        s = np.linspace(s1, s2, sn)
        b = np.linspace(b1, b2, bn) * d2r
        bp = b - np.pi
        tmp = -2j * np.pi * f
        b0 = (b0-180) * d2r
        pos = super().relative_position(self.xy, ptype=ptype, sys=self.sys)
        p = np.zeros((sn, bn), dtype=complex)
        B, S = np.meshgrid(bp, s)
        for i in range(len(pos[:, 0])):
                shift = pos[i, 0] * (S*np.sin(B)-s0*np.sin(b0)) + \
                        pos[i, 1] * (S*np.cos(B)-s0*np.cos(b0))
                p += np.exp(tmp*shift)
        return b, s, p

    def general_band_response(self, f1=0.01, f2=0.05, df=1e-2,
                              s1=0, s2=1e-3, b1=0, b2=360,
                              s0=0, b0=90, sn=51, bn=121, ptype=0):
        d2r = np.pi / 180.
        s = np.linspace(s1, s2, sn)
        b = np.linspace(b1, b2, bn) * d2r
        bp = b - np.pi
        b0 = (b0 - 180) * d2r
        pos = super().relative_position(self.xy, ptype=ptype, sys=self.sys)
        p = np.zeros((sn, bn), dtype=complex)
        B, S = np.meshgrid(bp, s)
        n = len(pos[:, 0])
        shift = np.zeros((n, sn, bn))
        for i in range(n):
            shift[i] = pos[i, 0] * (S * np.sin(B) - s0 * np.sin(b0)) + \
                       pos[i, 1] * (S * np.cos(B) - s0 * np.cos(b0))
        f = f1
        while f <= f2:
            tmp = -2j * np.pi * f
            for i in range(n):
                    p += np.exp(tmp*shift[i])
            f += df
        return b, s, p


class Beamforming(BasicOperation):
    def __init__(self, xy, sys):
        super().check_input(xy, sys)
        self.xy = xy
        self.sys = sys

    def __cross_spectra(self, fd):
        n = len(fd[:, 0])
        cfd = []
        for i in range(n-1):
            for j in range(i+1, n):
                cfd.append(fd[i]*np.conjugate(fd[j]))
        return np.array(cfd)

    def harmonic_beam(self, fd, fs, f=0.05, s1=0, s2=1e-3, sn=51,
                       b1=0, b2=360, bn=121, ptype='01'):
        nf = len(fd[0])
        fn = int(f * nf / fs)
        if ptype == '01':
            pos = super().relative_position(self.xy, sys=self.sys)
        else:
            pos = super().cross_position(self.xy, sys=self.sys)
            fd = self.__cross_spectra(fd)
        fd = fd[:, fn]
        s = np.linspace(s1, s2, sn)
        b = np.linspace(b1, b2, bn) * np.pi / 180
        bp = b - np.pi
        B, S = np.meshgrid(bp, s)
        tmp = -2j * np.pi * f
        p = np.zeros((sn, bn), dtype=complex)
        for i in range(len(fd)):
            shift = S * (pos[i, 0] * np.sin(B) + pos[i, 1] * np.cos(B))
            p += fd[i]*np.exp(tmp*shift)
        return b, s, p

    def band_beam(self, fd, fs, f1=0.02, f2=0.06,
                  s1=0, s2=1e-3, sn=51, b1=0, b2=360, bn=121, ptype='01'):
        nf = len(fd[0])
        fn1 = int(f1 * nf / fs)
        fn2 = int(f2 * nf / fs)
        if ptype == '01':
            pos = super().relative_position(self.xy, sys=self.sys)
        else:
            pos = super().cross_position(self.xy, sys=self.sys)
            fd = self.__cross_spectra(fd)
        fd = fd[:, fn1+fn2+1]
        s = np.linspace(s1, s2, sn)
        b = np.linspace(b1, b2, bn) * np.pi / 180
        bp = b - np.pi
        B, S = np.meshgrid(bp, s)
        p = np.zeros((sn, bn), dtype=complex)
        for k in range(fn1, fn2+1):
            f = k * fs / nf
            tmp = -2j * np.pi * f
            for i in range(len(fd)):
                shift = S * (pos[i, 0] * np.sin(B) + pos[i, 1] * np.cos(B))
                p += fd[i, k]*np.exp(tmp*shift)
        return b, s, p