#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

PROCESS IMage

"""

import math
import numpy as np
from reproject import reproject_interp
import subprocess as SP

from astylo.sinout import read_fits, write_fits, WCSextract, write_csv
from astylo.myfunclib import fclean, closest


def wclean(filIN, wmod=0, filOUT=None):
	"""
	Clean wavelengths
	"""
	hdr, data, wave = read_fits(filIN, wmod=wmod)

	ind = []
	k = 0
	flag = 0
	for i in range(np.size(wave)-1):
		## check if delete wave[i+1]
		if wave[k]>=wave[i+1]:
			ind.append(i+1)
			flag += 1
			if flag==1:
				ind.append(k)
		## if not delete, shift ref wave[k]
		else:
			k = i+1
			flag = 0
	print('Number of wave to delete: ', np.size(ind))
	# for i in ind:
	# 	print(wave[i]+', ')

	data = np.delete(data, ind, axis=0)
	wave = np.delete(np.array(wave), ind)
	wave = list(wave)

	if filOUT is not None:
		write_fits(filOUT, hdr, data, wave)

	return data, wave

def specorrect(filIN, filOUT=None, \
	factor=None, zero=None, wmin=None, wmax=None, wmod=0):
	"""
	calibrate spectra from different obs. in order to eliminate gaps
	[optional] im = factor * im + zero
	"""
	im, wvl, hdr = read_fits(file=filIN, wmod=wmod)
	if wmin is None:
		wmin = wvl[0]
	if wmax is None:
		wmax = wvl[-1]
	
	if factor is not None:
		if zero is not None:
			for k, lam in enumerate(wvl):
				if lam>=wmin and lam<=wmax:
					im[k,:,:] = factor * im[k,:,:] + zero
		else:
			for k, lam in enumerate(wvl):
				if lam>=wmin and lam<=wmax:
					im[k,:,:] *= factor
	else:
		if zero is not None:
			for k, lam in enumerate(wvl):
				if lam>=wmin and lam<=wmax:
					im[k,:,:] += zero
	
	if filOUT is not None:
		write_fits(filOUT, hdr, im, wave=wvl)

	return im

def hextract(filIN, filOUT, x0, x1, y0, y1):
	"""
	crop 2D image with pixel sequence numbers
	[ref]
	IDL lib hextract
	https://idlastro.gsfc.nasa.gov/ftp/pro/astrom/hextract.pro
	"""
	oldim = read_fits(filIN)[0]
	hdr, w = WCSextract(filIN)[0:2]
	# hdr['NAXIS1'] = x1 - x0 + 1
	# hdr['NAXIS2'] = y1 - y0 + 1
	hdr['CRPIX1'] += -x0
	hdr['CRPIX2'] += -y0
	newim = oldim[y0:y1+1, x0:x1+1]

	write_fits(filOUT, hdr, newim)

	return newim

##-----------------------------------------------

##			IMPROVE based tools

##-----------------------------------------------

class improve:
	"""
	IMage PROcessing VEssel
	"""
	def __init__(self, filIN, wmod=0):
		
		## INPUTS
		self.filIN = filIN
		self.wmod = wmod

		## read image/cube
		## self.hdr is a 2D (reduced) header
		self.hdr, self.w, self.is3d = WCSextract(filIN)
		self.NAXIS1 = self.hdr['NAXIS1']
		self.NAXIS2 = self.hdr['NAXIS2']
		print("Raw size (pix): {} * {}".format(
			self.NAXIS1, self.NAXIS2))
		## 3D cube slicing
		if self.is3d==True:
			self.im, self.wvl = read_fits(filIN, wmod=wmod)[1:3]
			self.NAXIS3 = np.size(self.wvl)
		else:
			self.im = read_fits(filIN, wmod=wmod)[1]
			self.wvl = None

	def uncadd(self, uncIN=None, wmod=0):
		## uncertainty adding
		mu, sigma = 0., 1.

		if uncIN is not None:
			unc = read_fits(uncIN, wmod)[1]
			theta = np.random.normal(mu, sigma, \
				self.NAXIS1*self.NAXIS2).reshape(
				self.NAXIS2, self.NAXIS1)
			## unc has the same dimension with im
			if self.is3d==True:
				for k in range(self.NAXIS3):
					self.im[k,:,:] += theta * unc[k,:,:]
			else:
				self.im += theta * unc

	def slice(self, filSL, suffix=None):
		## 3D cube slicing
		if self.is3d==True:
			slicnames = []
			for k in range(self.NAXIS3):
				## output filename list
				f = filSL+'_'+'0'*(4-len(str(k)))+str(k)
				if suffix is not None:
					f += suffix
				slicnames.append(f)
				# comment = "NO.{} image sliced from {}.fits".format(k, self.filIN)
				write_fits(f, self.hdr, self.im[k,:,:])
		else:
			print('Input file is a 2D image which cannot be sliced! ')
			exit()

		return slicnames
	
	def rectangle(self, cen, size, filOUT=None):
		## rectangle center in (ra, dec)
		## rectangle size in pix
		## [optional] 2D raw data to crop
		print("Crop centre (ra, dec): [{:.8}, {:.8}]".format(*cen))
		print("Crop size (pix): [{}, {}].".format(*size))
		
		## convert coord
		xcen, ycen = self.w.all_world2pix(cen[0], cen[1], 1)
		if not (0<xcen<self.NAXIS1 and 0<ycen<self.NAXIS2):
			print("Error: crop centre overpassed image border! ")
			exit()
		## lowerleft origin
		xmin = math.floor(xcen - size[0]/2.)
		ymin = math.floor(ycen - size[1]/2.)
		xmax = xmin + size[0]
		ymax = ymin + size[1]
		if not (xmin>=0 and xmax<=self.NAXIS1 and ymin>=0 and ymax<=self.NAXIS2):
			print("Error: crop region overpassed image border! ")
			exit()

		## OUTPUTS
		##---------
		## new image
		if self.is3d==True:
			self.im = self.im[:, ymin:ymax, xmin:xmax]
			## recover 3D non-reduced header
			self.hdr = read_fits(self.filIN, self.wmod)[0]
		else:
			self.im = self.im[ymin:ymax, xmin:xmax]
		## modify header
		self.hdr['CRPIX1'] += -xmin
		self.hdr['CRPIX2'] += -ymin
		## write cropped image/cube
		if filOUT is not None:
			comment = "Image cropped at centre: [{:.8}, {:.8}]. ".format(*cen)
			comment = "with size [{}, {}] (pix).".format(*size)

			write_fits(filOUT, self.hdr, self.im, wave=self.wvl, \
				COMMENT=comment)

		return self.im

class slicube(improve):
	"""
	SLIce CUBE
	"""
	def __init__(self, filIN, filSL, wmod=0, \
		uncIN=None, wmod_unc=0, suffix=None):
		super().__init__(filIN, wmod)
		
		self.uncadd(uncIN, wmod_unc)

		self.slicnames = self.slice(filSL, suffix)

	def image(self):
		return self.im

	def wave(self):
		return self.wvl

	def slice_names(self):
		return self.slicnames

class crop(improve):
	"""
	CROP 2D image or 3D cube
	"""
	def __init__(self, filIN, cen, size, \
		wmod=0, uncIN=None, wmod_unc=0, \
		shape='box', filOUT=None):
		## slicrop: slice 
		super().__init__(filIN, wmod)

		self.uncadd(uncIN, wmod_unc)
		
		if shape=='box':
			self.cropim = self.rectangle(cen, size, filOUT)

	def image(self):
		return self.cropim

	def wave(self):
		return self.wvl

class project(improve):
	"""
	PROJECT 2D image or 3D cube
	"""
	def __init__(self, filIN, filREF=None, hdREF=None, \
		wmod=0, uncIN=None, wmod_unc=0, filTMP=None, filOUT=None):
		super().__init__(filIN, wmod)
		## input hdREF must be (reduced) 2D header
		self.uncadd(uncIN, wmod_unc)

		if filREF is not None:
			hdREF = WCSextract(filREF)[0]
			hdREF['EQUINOX'] = 2000.0
		
		if hdREF is not None:
			if self.is3d==True:
				if filTMP is not None:
					filSL = filTMP
				else:
					filSL = self.filIN
				slicIN = self.slice(filSL=filSL, suffix='_')
				im = []
				self.slicnames = []
				for f in slicIN:
					im.append(reproject_interp(f+'.fits', hdREF)[0])
					if filTMP is not None:
						write_fits(f+'_rep', hdREF, im)
						self.slicnames.append(f+'_rep')
					fclean(f+'.fits')

				self.projim = np.array(im)
				## recover non-reduced 3D header
				if filREF is not None:
					hdr = read_fits(filREF, self.wmod)[0]
			else:
				self.projim, footprint = reproject_interp(filIN+'.fits', hdREF)
			
		if filOUT is not None:
			comment = "Reprojected image. "
			
			if self.is3d==True:
				write_fits(filOUT, hdr, self.projim, wave=self.wvl, \
					COMMENT=comment)
			else:
				write_fits(filOUT, hdREF, self.projim, wave=self.wvl, \
					COMMENT=comment)
	
	def image(self):
		return self.projim

	def wave(self):
		return self.wvl

	def slice_names(self):
		return self.slicnames

class iconvolve(improve):
	"""
	(IDL based) CONVOLVE 2D image or 3D cube with given kernels
	"""
	def __init__(self, filIN, filKER, saveKER, \
		wmod=0, uncIN=None, wmod_unc=0, \
		psf=None, filTMP=None, filOUT=None):
		## INPUTS
		super().__init__(filIN, wmod)
		
		self.uncadd(uncIN, wmod_unc)

		## input kernel file list
		self.filKER = list(filKER)
		## doc (csv) file of kernel list
		self.saveKER = saveKER
		self.filTMP = filTMP
		self.filOUT = filOUT

		## INIT
		if psf is None:
			self.psf = [2.,2.5,3.,3.5,4.,4.5,5.,5.5,6.]
		else:
			self.psf = psf
		self.sig_lam = None
				
	def spitzer_irs(self):
		"""
		Spitzer/IRS PSF profil
		[ref]
		Pereira-Santaella, Miguel, Almudena Alonso-Herrero, George H.
		Rieke, Luis Colina, Tanio Díaz-Santos, J.-D. T. Smith, Pablo G.
		Pérez-González, and Charles W. Engelbracht. “Local Luminous
		Infrared Galaxies. I. Spatially Resolved Observations with the
		Spitzer Infrared Spectrograph.” The Astrophysical Journal
		Supplement Series 188, no. 2 (June 1, 2010): 447.
		doi:10.1088/0067-0049/188/2/447.
		"""
		sig_par_wave = [0, 13.25, 40.]
		sig_par_fwhm = [2.8, 3.26, 10.1]
		sig_per_wave = [0, 15.5, 40.]
		sig_per_fwhm = [3.8, 3.8, 10.1]
		
		## fwhm (arcsec)
		fwhm_par = np.interp(self.wvl, sig_par_wave, sig_par_fwhm)
		fwhm_per = np.interp(self.wvl, sig_per_wave, sig_per_fwhm)
		#fwhm_lam = np.sqrt(fwhm_par * fwhm_per)
		
		## sigma (arcsec)
		sig_par = fwhm_par / (2. * np.sqrt(2.*np.log(2.)))
		sig_per = fwhm_per / (2. * np.sqrt(2.*np.log(2.)))
		self.sig_lam = np.sqrt(sig_par * sig_per)
		
	def choker(self, filIN):
		## CHOose KERnel (list)

		## create list
		klist = []
		for i, image in enumerate(filIN):
			## check PSF profil (or is not a cube)
			if self.sig_lam is not None:
				image = filIN[i]
				ind = closest(self.psf, self.sig_lam[i])
				kernel = self.filKER[ind]
			else:
				image = filIN[0]
				kernel = self.filKER[0]
			## klist line elements: image, kernel
			k = [image, kernel]
			klist.append(k)

		## write csv file
		write_csv(self.saveKER, header=['Images', 'Kernels'], data=klist)

	def do_conv(self, ipath):
		
		if self.is3d==True:
			if self.filTMP is not None:
				filSL = self.filTMP
			else:
				filSL = self.filIN
			
			slicIN = self.slice(filSL)
			self.spitzer_irs()
			self.choker(slicIN)
		else:
			if self.filTMP is not None: # ?? TO DELETE
				filIN = [self.filTMP]
			else:
				filIN = [self.filIN]
			
			self.choker(filIN)

		SP.call('cd '+ipath+'\nidl conv.pro', shell=True)

		## OUTPUTS
		##---------
		if self.is3d==True:
			im = []
			self.slicnames = []
			for f in slicIN:
				im.append(read_fits(f+'_conv')[1])
				self.slicnames.append(f+'_conv')

			self.convim = np.array(im)
			## recover non-reduced 3D header
			self.hdr = read_fits(self.filIN, self.wmod)[0]
		else:
			self.convim = read_fits(self.filIN+'_conv')[1]
		
		if self.filOUT is not None:
			comment = "Image convolved by G. Aniano's IDL routine."
			comment = 'https://www.astro.princeton.edu/~ganiano/Kernels.html'

			write_fits(self.filOUT, self.hdr, self.convim, wave=self.wvl, \
				COMMENT=comment)

	def image(self):
		return self.convim

	def wave(self):
		return self.wvl

	def slice_names(self):
		return self.slicnames

"""
------------------------------ MAIN (test) ------------------------------
"""
if __name__ == "__main__":

	pass
