# -*- coding: utf-8 -*-
"""This module defines functions for Dali searching Protein Data Bank."""

import re
import numpy as np
from prody.atomic import Atomic, AtomGroup, AtomMap
from prody.measure import getRMSD, getTransformation
from prody.utilities import checkCoords, checkWeights
from prody import LOGGER, PY3K
from prody import parsePDB
if PY3K:
    import urllib.parse as urllib
    import urllib.request as urllib2
else:
    import urllib
    import urllib2
from .ensemble import Ensemble
from .pdbensemble import PDBEnsemble
import os

__all__ = ['daliRecord', 'searchDali']

def searchDali(pdbId, chainId, daliURL=None, subset='fullPDB', **kwargs):
    """Search Dali server with input of PDB ID and chain ID.
    Dali server: http://ekhidna2.biocenter.helsinki.fi/dali/
    
    :arg subset: fullPDB, PDB25, PDB50, PDB90
    :type sequence: str"""
    LOGGER.timeit('_dali')
    # timeout = 120
    timeout = kwargs.pop('timeout', 120)
    
    if daliURL is None:
        daliURL = "http://ekhidna2.biocenter.helsinki.fi/cgi-bin/sans/dump.cgi"
    pdbId = pdbId.lower()
    pdb_chain = pdbId + chainId
    parameters = { 'cd1' : pdb_chain, 'method': 'search', 'title': 'Title_'+pdb_chain, 'address': '' }
    enc_params = urllib.urlencode(parameters).encode('utf-8')
    request = urllib2.Request(daliURL, enc_params)
    try_error = 3
    while try_error >= 0:
        try:
            url = urllib2.urlopen(request).url
            break
        except:
            try_error -= 1
            if try_error >= 0:
                LOGGER.sleep(2, '. Connection error happened. Trying to reconnect...')
                continue
            else:
                url = urllib2.urlopen(request).url
                break
    if url.split('.')[-1].lower() in ['html', 'php']:
        # print('test -1: '+url)
        url = url.replace(url.split('/')[-1], '')
    LOGGER.debug('Submitted Dali search for PDB and chain "{0} and {1}".'.format(pdbId, chainId))
    LOGGER.info(url)
    LOGGER.clear()
    obj = daliRecord(url, pdbId, chainId, subset=subset, timeout=timeout, **kwargs)
    if obj.isSuccess:
        return obj
    
    return None

class daliRecord(object):

    """A class to store results from Dali PDB search."""

    def __init__(self, url, pdbId=None, chainId=None, subset='fullPDB', localFile=False, **kwargs):
        """Instantiate a daliPDB object instance.

        :arg url: url of Dali results page or local dali results file.
        :arg pdbId: PDB code for searched protein.
        :arg chainId: chain identifier (only one chain can be assigned for PDB).
        :arg subset: fullPDB, PDB25, PDB50, PDB90. Ignored if localFile=True (url is a local file).
        :arg localFile: provided url is a path for local dali results file.
        """

        self._url = url
        self._pdbId = pdbId
        # self._chainId = chainId
        self._chainId = chainId.upper()
        subset = subset.upper()
        if subset == "FULLPDB" or subset not in ["PDB25", "PDB50", "PDB90"]:
            self._subset = ""
        else:
            self._subset = "-"+subset[3:]
        timeout = kwargs.pop('timeout', 120)
        self.isSuccess = self.getRecord(self._url, localFile=localFile, timeout=timeout, **kwargs)

    def getRecord(self, url, localFile=False, **kwargs):
        if localFile:
            dali_file = open(url, 'r')
            data = dali_file.read()
            dali_file.close()
        else:
            sleep = 2
            # timeout = 120
            timeout = kwargs.pop('timeout', 120)
            LOGGER.timeit('_dali')
            log_message = ''
            try_error = 3
            while True:
                LOGGER.sleep(int(sleep), 'to reconnect Dali '+log_message)
                LOGGER.clear()
                LOGGER.write('Connecting Dali for search results...')
                LOGGER.clear()
                try:
                    html = urllib2.urlopen(url).read()
                except:
                    try_error -= 1
                    if try_error >= 0:
                        LOGGER.sleep(2, '. Connection error happened. Trying to reconnect...')
                        continue
                    else:
                        html = urllib2.urlopen(url).read()
                if html.find('Status: Queued') > -1:
                    log_message = '(Dali searching is queued)...'
                elif html.find('Status: Running') > -1:
                    log_message = '(Dali searching is running)...'
                elif html.find('Your job') == -1 and html.find('.txt') > -1:
                    break
                elif html.find('ERROR:') > -1:
                    LOGGER.warn(': Dali search reported an ERROR!')
                    return None
                sleep = 20 if int(sleep * 1.5) >= 20 else int(sleep * 1.5)
                if LOGGER.timing('_dali') > timeout:
                    LOGGER.warn(': Dali search is time out. \nThe results can be obtained using getRecord() function later.')
                    return None
                LOGGER.clear()
            LOGGER.clear()
            LOGGER.report('Dali results completed in %.1fs.', '_dali')
            lines = html.strip().split('\n')
            file_name = re.search('=.+-90\.txt', html).group()[1:]
            file_name = file_name[:-7]
            # LOGGER.info(url+file_name+self._subset+'.txt')
            data = urllib2.urlopen(url+file_name+self._subset+'.txt').read()
            localfolder = kwargs.pop('localfolder', '.')
            temp_name = file_name+self._subset+'_dali.txt'
            if localfolder != '.' and not os.path.exists(localfolder):
                os.mkdir(localfolder)
            with open(localfolder+os.sep+temp_name, "w") as file_temp: file_temp.write(html + '\n' + url+file_name + '\n' + data)
            # with open(temp_name, "a+") as file_temp: file_temp.write(url+file_name + '\n' + data)
        data_list = data.strip().split('# ')
        # No:  Chain   Z    rmsd lali nres  %id PDB  Description -> data_list[3]
        # Structural equivalences -> data_list[4]
        # Translation-rotation matrices -> data_list[5]
        map_temp_dict = dict()
        mapping = []
        lines = data_list[4].strip().split('\n')
        self._lines_4 = lines
        mapping_temp = np.genfromtxt(lines[1:], delimiter = (4,1,14,6,2,4,4,5,2,4,4,3,5,4,3,5,6,3,5,4,3,5,28), usecols = [0,3,5,7,9,12,15,15,18,21], dtype='|i4')
        # [0,3,5,7,9,12,15,15,18,21] -> [index, residue_a, residue_b, residue_i_a, residue_i_b, resid_a, resid_b, resid_i_a, resid_i_b]
        for map_i in mapping_temp:
            if not map_i[0] in map_temp_dict:
                map_temp_dict[map_i[0]] = [[map_i[1], map_i[2], map_i[3], map_i[4]]]
            else:
                map_temp_dict[map_i[0]].append([map_i[1], map_i[2], map_i[3], map_i[4]])
        self._max_index = max(mapping_temp[:,2])
        self._mapping = map_temp_dict
        self._data = data_list[3]
        lines = data_list[3].strip().split('\n')
        daliInfo = np.genfromtxt(lines[1:], delimiter = (4,3,6,5,5,5,6,5,57), usecols = [0,2,3,4,5,6,7,8], dtype=[('id', '<i4'), ('pdb_chain', '|S6'), ('Z', '<f4'), ('rmsd', '<f4'), ('len_align', '<i4'), ('res_num', '<i4'), ('identity', '<i4'), ('title', '|S70')])
        if daliInfo.ndim == 0:
            daliInfo = np.array([daliInfo])
        pdbListAll = []
        self._daliInfo = daliInfo
        dali_temp_dict = dict()
        for temp in self._daliInfo:
            temp_dict = dict()
            pdb_chain = temp[1].strip()[0:6]
            temp_dict['pdbId'] = pdb_chain[0:4]
            temp_dict['chainId'] = pdb_chain[5:6]
            temp_dict['pdb_chain'] = pdb_chain
            temp_dict['Z'] = temp[2]
            temp_dict['rmsd'] = temp[3]
            temp_dict['len_align'] = temp[4]
            temp_dict['res_num'] = temp[5]
            temp_dict['identity'] = temp[6]
            temp_dict['mapping'] = (np.array(map_temp_dict[temp[0]])-1).tolist()
            temp_dict['map_ref'] = [x for map_i in (np.array(map_temp_dict[temp[0]])-1).tolist() for x in range(map_i[0], map_i[1]+1)]
            temp_dict['map_sel'] = [x for map_i in (np.array(map_temp_dict[temp[0]])-1).tolist() for x in range(map_i[2], map_i[3]+1)]
            dali_temp_dict[temp_dict['pdb_chain']] = temp_dict
            pdbListAll.append(pdb_chain)
        self._pdbListAll = tuple(pdbListAll)
        self._pdbList = self._pdbListAll
        self._alignPDB = dali_temp_dict
        LOGGER.info('Obtained ' + str(len(pdbListAll)) + ' PDB chains from Dali for '+self._pdbId+self._chainId+'.')
        return True
        
    def getPDBList(self):
        """Returns PDB list (filters may applied)"""
        return self._pdbList
        
    def getPDBListAll(self):
        """Returns all PDB list"""
        return self._pdbListAll
        
    def getHits(self):
        return self._alignPDB
        
    def getFilterList(self):
        filterDict = self._filterDict
        temp_str = ', '.join([str(len(filterDict['len'])), str(len(filterDict['rmsd'])), str(len(filterDict['Z'])), str(len(filterDict['identity']))])
        LOGGER.info('Filter out [' + temp_str + '] for [length, RMSD, Z, identity]')
        return self._filterList
        
    def filter(self, cutoff_len=None, cutoff_rmsd=None, cutoff_Z=None, cutoff_identity=None):
        """Filters out PDBs from the PDBList and returns the PDB list.
        PDBs satisfy any of following criterion will be filtered out.
        (1) Length of aligned residues < cutoff_len; cutoff_len must be a ratio of length (between 0 and 1), or a length of aligned residues; (0.8)
        (2) RMSD < cutoff_rmsd; (1.0)
        (3) Z score < cutoff_Z; (20)
        (4) Identity < cutoff_identity. (90)
        """
        if cutoff_len == None:
            cutoff_len = int(0.8*self._max_index)
        elif not isinstance(cutoff_len, (float, int)):
            raise TypeError('cutoff_len must be a float or an integer')
        elif cutoff_len <= 1 and cutoff_len > 0:
            cutoff_len = int(cutoff_len*self._max_index)
        elif cutoff_len <= self._max_index and cutoff_len > 0:
            cutoff_len = int(cutoff_len)
        else:
            raise ValueError('cutoff_len must be a float between 0 and 1, or an int not greater than the max length')
            
        if cutoff_rmsd == None:
            cutoff_rmsd = 0
        elif not isinstance(cutoff_rmsd, (float, int)):
            raise TypeError('cutoff_rmsd must be a float or an integer')
        elif cutoff_rmsd >= 0:
            cutoff_rmsd = float(cutoff_rmsd)
        else:
            raise ValueError('cutoff_rmsd must be a number not less than 0')
            
        if cutoff_Z == None:
            cutoff_Z = 0
        elif not isinstance(cutoff_Z, (float, int)):
            raise TypeError('cutoff_Z must be a float or an integer')
        elif cutoff_Z >= 0:
            cutoff_Z = float(cutoff_rmsd)
        else:
            raise ValueError('cutoff_Z must be a number not less than 0')
            
        if cutoff_identity == None or cutoff_identity == 0:
            cutoff_identity = 100
        elif not isinstance(cutoff_identity, (float, int)):
            raise TypeError('cutoff_identity must be a float or an integer')
        elif cutoff_identity <= 1 and cutoff_len > 0:
            cutoff_identity = float(cutoff_len*100)
        elif cutoff_identity <= 100 and cutoff_len > 0:
            cutoff_identity = float(cutoff_identity)
        else:
            raise ValueError('cutoff_identity must be a float between 0 and 1, or a number between 0 and 100')
            
        daliInfo = self._alignPDB
        pdbListAll = self._pdbListAll
        missing_ind_dict = dict()
        ref_indices_set = set(range(self._max_index))
        filterListLen = []
        filterListRMSD = []
        filterListZ = []
        filterListIdentiry = []
        
        # keep the first PDB (query PDB)
        for pdb_chain in pdbListAll[1:]:
            temp_dict = daliInfo[pdb_chain]
            # filter: len_align, identity, rmsd, Z
            if temp_dict['len_align'] < cutoff_len:
                # print('Filter out ' + pdb_chain + ', len_align: ' + str(temp_dict['len_align']))
                filterListLen.append(pdb_chain)
                continue
            if temp_dict['rmsd'] < cutoff_rmsd:
                # print('Filter out ' + pdb_chain + ', rmsd: ' + str(temp_dict['rmsd']))
                filterListRMSD.append(pdb_chain)
                continue
            if temp_dict['Z'] < cutoff_Z:
                # print('Filter out ' + pdb_chain + ', Z: ' + str(temp_dict['Z']))
                filterListZ.append(pdb_chain)
                continue
            if temp_dict['identity'] > cutoff_identity:
                # print('Filter out ' + pdb_chain + ', identity: ' + str(temp_dict['identity']))
                filterListIdentiry.append(pdb_chain)
                continue
            temp_diff = list(ref_indices_set - set(temp_dict['map_ref']))
            for diff_i in temp_diff:
                if not diff_i in missing_ind_dict:
                    missing_ind_dict[diff_i] = 1
                else:
                    missing_ind_dict[diff_i] += 1
        self._missing_ind_dict = missing_ind_dict
        filterList = filterListLen + filterListRMSD + filterListZ + filterListIdentiry
        filterDict = {'len': filterListLen, 'rmsd': filterListRMSD, 'Z': filterListZ, 'identity': filterListIdentiry}
        self._filterList = filterList
        self._filterDict = filterDict
        self._pdbList = [self._pdbListAll[0]] + list(set(list(self._pdbListAll[1:])) - set(filterList))
        LOGGER.info(str(len(filterList)) + ' PDBs have been filtered out from '+str(len(pdbListAll))+' Dali hits.')
        return self._pdbList
        
    def buildDaliEnsemble(self):
        daliInfo = self._alignPDB
        pdbList = self._pdbList

        n_confs = len(pdbList)
        LOGGER.progress('Building PDB ensemble for {0} conformations from Dali...'
                        .format(n_confs), n_confs, '_prody_buildDaliEnsemble')

        ref_pdb = parsePDB(self._pdbId).select('chain '+self._chainId).copy()

        ref_pdb_ca = ref_pdb.select("protein and name CA")
        if ref_pdb_ca is None:
            ref_pdb_ca = ref_pdb.select("name CA and not resname CA")
        ref_pdb_ca = ref_pdb_ca.copy()

        ref_chain = ref_pdb_ca.getHierView().getChain(self._chainId)
        ref_indices_set = set(range(len(ref_chain)))
        ensemble = PDBEnsemble('Dali ensemble - ' + str(self._pdbId) + '-' + str(self._chainId))
        ensemble.setAtoms(ref_chain)
        ensemble.setCoords(ref_chain)
        failPDBList = []
        
        for i in range(n_confs):
            pdb_chain = pdbList[i]
            temp_dict = daliInfo[pdb_chain]
            sel_pdb = parsePDB(pdb_chain[:4]).select('chain '+pdb_chain[5]).copy()
            try:
                sel_pdb_ca = sel_pdb.select("protein and name CA").copy()
            except:
                sel_pdb_ca = sel_pdb.select("name CA and not resname CA").copy()
            map_ref = temp_dict['map_ref']
            map_sel = temp_dict['map_sel']
            dum_sel = list(ref_indices_set - set(map_ref))
            atommap = AtomMap(sel_pdb_ca, indices=map_sel, mapping=map_ref, dummies=dum_sel)
            try:
                ensemble.addCoordset(atommap, weights=atommap.getFlags('mapped'), degeneracy=True)
            except:
                failPDBList.append(pdb_chain)
            LOGGER.update(i, label='_prody_buildDaliEnsemble')
        LOGGER.finish()
        self._failPDBList = failPDBList
        if failPDBList != []:
            LOGGER.warn('failed to add ' + str(len(failPDBList)) + 
                        ' PDB chain to ensemble: ' + ' '.join(failPDBList))
        try:
            ensemble.iterpose()
            RMSDs = ensemble.getRMSDs()
        except:
            LOGGER.warn('failed to iterpose the ensemble.')
            
        return ensemble
