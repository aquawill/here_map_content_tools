from here.content.utils.hmc_external_references import HMCExternalReferences
from here.platform.adapter import Identifier
from here.platform.adapter import Partition
from here.platform.adapter import Ref

hmc_external_reference = HMCExternalReferences()

partition_id = '24134137'
segment_id = 'here:cm:segment:826153057'

pvid = hmc_external_reference.segment_to_pvid(partition_id=partition_id,
                                              segment_ref=Ref(partition=Partition(str(partition_id)),
                                                              identifier=Identifier(segment_id)))
segment = hmc_external_reference.pvid_to_segment(partition_id=partition_id, pvid=973157480)

print(pvid)
print(segment.identifier)
