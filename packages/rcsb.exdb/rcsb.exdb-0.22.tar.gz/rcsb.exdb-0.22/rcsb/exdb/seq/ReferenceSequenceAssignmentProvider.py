##
# File: ReferenceSequenceAssignmentProvider.py
# Date: 8-Oct-2019  jdw
#
# Utilities to cache content required to update referencence sequence assignments.
#
# Updates:
#
##
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
from collections import defaultdict


from rcsb.exdb.utils.ObjectExtractor import ObjectExtractor
from rcsb.utils.io.MarshalUtil import MarshalUtil
from rcsb.utils.seq.SiftsSummaryProvider import SiftsSummaryProvider
from rcsb.utils.seq.UniProtUtils import UniProtUtils

logger = logging.getLogger(__name__)


class ReferenceSequenceAssignmentProvider(object):
    """  Utilities to cache content required to update referencence sequence assignments.

    """

    def __init__(
        self,
        cfgOb,
        databaseName="pdbx_core",
        collectionName="pdbx_core_entity",
        polymerType="Protein",
        referenceDatabaseName="UniProt",
        provSource="PDB",
        maxChunkSize=350,
        fetchLimit=None,
        **kwargs
    ):
        self.__cfgOb = cfgOb
        self.__polymerType = polymerType
        self.__mU = MarshalUtil()
        #
        self.__maxChunkSize = maxChunkSize
        self.__statusList = []
        #
        self.__ssP = self.__fetchSiftsSummaryProvider(self.__cfgOb, self.__cfgOb.getDefaultSectionName(), **kwargs)
        self.__refIdMapD, self.__refD, self.__matchD = self.__reload(databaseName, collectionName, polymerType, referenceDatabaseName, provSource, fetchLimit, **kwargs)

    def getSiftsSummaryProvider(self):
        return self.__ssP

    def getMatchInfo(self):
        return self.__matchD

    def getRefData(self):
        return self.__refD

    def getRefIdMap(self):
        return self.__refIdMapD

    def getRefDataCount(self):
        return len(self.__refD)

    def testCache(self):
        ok = self.__refIdMapD and self.__matchD and self.__refD and len(self.__refIdMapD) >= len(self.__matchD)
        logger.info("Status %r Lengths: refIdMap %d matchD %d refD %d", ok, len(self.__refIdMapD), len(self.__matchD), len(self.__refD))
        ok = self.__refIdMapD and self.__matchD and self.__refD and len(self.__refIdMapD) >= len(self.__matchD)
        return ok

    def __reload(self, databaseName, collectionName, polymerType, referenceDatabaseName, provSource, fetchLimit, **kwargs):
        assignRefD = self.__getPolymerReferenceSequenceAssignments(databaseName, collectionName, polymerType, fetchLimit)
        refIdMapD, _ = self.__getAssignmentMap(assignRefD, referenceDatabaseName=referenceDatabaseName, provSource=provSource)
        #
        #
        refD, matchD = self.__rebuildReferenceCache(list(refIdMapD.keys()), referenceDatabaseName, **kwargs)
        return refIdMapD, matchD, refD

    def __getPolymerReferenceSequenceAssignments(self, databaseName, collectionName, polymerType, fetchLimit):
        """ Get all accessions assigned to input reference sequence database for the input polymerType.

            Returns:
             (dict): {"1abc_1": "rcsb_entity_container_identifiers": {"reference_sequence_identifiers": []},
                                "rcsb_polymer_entity_align": [],
                                "rcsb_entity_source_organism"" {"ncbi_taxonomy_id": []}
        """
        try:
            obEx = ObjectExtractor(
                self.__cfgOb,
                databaseName=databaseName,
                collectionName=collectionName,
                cacheFilePath=None,
                useCache=False,
                keyAttribute="entity",
                uniqueAttributes=["rcsb_id"],
                cacheKwargs=None,
                objectLimit=fetchLimit,
                selectionQuery={"entity_poly.rcsb_entity_polymer_type": polymerType},
                selectionList=[
                    "rcsb_id",
                    "rcsb_entity_container_identifiers.reference_sequence_identifiers",
                    "rcsb_entity_container_identifiers.auth_asym_ids",
                    "rcsb_polymer_entity_align",
                    "rcsb_entity_source_organism.ncbi_taxonomy_id",
                ],
            )
            eCount = obEx.getCount()
            logger.info("Entity count is %d", eCount)
            objD = obEx.getObjects()
            logger.info("Reading polymer entity entity count %d ref accession length %d ", eCount, len(objD))
            #
        except Exception as e:
            logger.exception("Failing for %s (%s) with %s", databaseName, collectionName, str(e))
        return objD

    def __getAssignmentMap(self, objD, referenceDatabaseName="UniProt", provSource="PDB"):
        refIdD = defaultdict(list)
        taxIdD = defaultdict(list)
        numMissing = 0
        for entityKey, eD in objD.items():
            try:
                accS = set()
                for ii, tD in enumerate(eD["rcsb_entity_container_identifiers"]["reference_sequence_identifiers"]):
                    if tD["database_name"] == referenceDatabaseName and tD["provenance_source"] == provSource:
                        accS.add(tD["database_accession"])
                        refIdD[tD["database_accession"]].append(entityKey)
                        #
                        # pick up the corresponding taxonomy -
                        try:
                            taxIdD[tD["database_accession"]].append(eD["rcsb_entity_source_organism"][ii]["ncbi_taxonomy_id"])
                        except Exception:
                            logger.warning("Failing taxonomy lookup for %s %r", entityKey, tD["database_accession"])

                logger.debug("PDB assigned sequences length %d", len(accS))
            except Exception as e:
                numMissing += 1
                logger.debug("No sequence assignments for %s with %s", entityKey, str(e))
        #
        for refId, taxIdL in taxIdD.items():
            taxIdL = list(set(taxIdL))
            if len(taxIdL) > 1:
                logger.info("Multitple taxIds assigned to reference sequence id %s: %r", refId, taxIdL)

        logger.info("Unique %s accession assignments by %s %d (missing %d) ", referenceDatabaseName, provSource, len(refIdD), numMissing)
        return refIdD, taxIdD

    #
    def __rebuildReferenceCache(self, idList, refDbName, **kwargs):
        """
        """
        doMissing = True
        dD = {}
        cachePath = kwargs.get("cachePath", ".")
        dirPath = os.path.join(cachePath, "exdb")
        # cacheKwargs = kwargs.get("cacheKwargs", {"fmt": "json", "indent": 3})
        cacheKwargs = kwargs.get("cacheKwargs", {"fmt": "pickle"})
        useCache = kwargs.get("useCache", True)
        saveText = kwargs.get("saveText", False)
        #
        ext = "pic" if cacheKwargs["fmt"] == "pickle" else "json"
        fn = refDbName + "-ref-sequence-data-cache" + "." + ext
        dataCacheFilePath = os.path.join(dirPath, fn)
        #
        fn = refDbName + "-ref-sequence-id-cache" + ".json"
        accCacheFilePath = os.path.join(dirPath, fn)
        #
        self.__mU.mkdir(dirPath)
        if not useCache:
            for fp in [dataCacheFilePath, accCacheFilePath]:
                try:
                    os.remove(fp)
                except Exception:
                    pass
        #
        if useCache and accCacheFilePath and self.__mU.exists(accCacheFilePath) and dataCacheFilePath and self.__mU.exists(dataCacheFilePath):
            dD = self.__mU.doImport(dataCacheFilePath, **cacheKwargs)
            idD = self.__mU.doImport(accCacheFilePath, fmt="json")
            logger.info("Reading cached reference sequence ID and data cache files %d", len(idD["matchInfo"]))
            # Check for completeness -
            if doMissing:
                missingS = set(idD["matchInfo"].keys()) - set(idList)
                if missingS:
                    logger.info("Reference sequence cache missing %d accessions", len(missingS))
                    extraD, extraIdD = self.__fetchReferenceEntries(refDbName, list(missingS), saveText=saveText, fetchLimit=None)
                    dD["refDbCache"].update(extraD["refDbCache"])
                    idD["matchInfo"].update(extraIdD["matchInfo"])
                    if accCacheFilePath and dataCacheFilePath and cacheKwargs:
                        self.__mU.mkdir(dirPath)
                        ok1 = self.__mU.doExport(dataCacheFilePath, dD, **cacheKwargs)
                        ok2 = self.__mU.doExport(accCacheFilePath, idD, fmt="json", indent=3)
                        logger.info("Cache updated with missing references with status %r", ok1 and ok2)
            #
        else:

            dD, idD = self.__fetchReferenceEntries(refDbName, idList, saveText=saveText, fetchLimit=None)
            if accCacheFilePath and dataCacheFilePath and cacheKwargs:
                self.__mU.mkdir(dirPath)
                ok1 = self.__mU.doExport(dataCacheFilePath, dD, **cacheKwargs)
                ok2 = self.__mU.doExport(accCacheFilePath, idD, fmt="json", indent=3)
                logger.info("Cache save status %r", ok1 and ok2)

        return idD["matchInfo"], dD["refDbCache"]

    def __fetchReferenceEntries(self, refDbName, idList, saveText=False, fetchLimit=None):
        """ Fetch database entries from the input reference sequence database name.
        """
        dD = {"refDbName": refDbName, "refDbCache": {}}
        idD = {"matchInfo": {}, "refIdMap": {}}

        try:
            idList = idList[:fetchLimit] if fetchLimit else idList
            logger.info("Starting fetch for %d %s entries", len(idList), refDbName)
            if refDbName == "UniProt":
                fobj = UniProtUtils(saveText=saveText)
                refD, matchD = fobj.fetchList(idList, maxChunkSize=self.__maxChunkSize)
                dD = {"refDbName": refDbName, "refDbCache": refD}
                idD = {"matchInfo": matchD}

        except Exception as e:
            logger.exception("Failing with %s", str(e))

        return dD, idD

    def __fetchSiftsSummaryProvider(self, cfgOb, configName, **kwargs):
        abbreviated = kwargs.get("siftsAbbreviated", "PROD")
        cachePath = kwargs.get("cachePath", ".")
        cacheKwargs = kwargs.get("cacheKwargs", {"fmt": "pickle"})
        useCache = kwargs.get("useCache", True)
        #
        srcDirPath = os.path.join(cachePath, cfgOb.getPath("SIFTS_SUMMARY_DATA_PATH", sectionName=configName))
        cacheDirPath = os.path.join(cachePath, cfgOb.get("SIFTS_SUMMARY_CACHE_DIR", sectionName=configName))
        logger.debug("ssP %r %r", srcDirPath, cacheDirPath)
        ssP = SiftsSummaryProvider(srcDirPath=srcDirPath, cacheDirPath=cacheDirPath, useCache=useCache, abbreviated=abbreviated, cacheKwargs=cacheKwargs)
        logger.info("ssP entry count %d", ssP.getEntryCount())
        return ssP
