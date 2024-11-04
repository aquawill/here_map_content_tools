from here.content.utils.hmc_external_references import HMCExternalReferences

from mapquadlib.herequad import HereQuad

hmc_external_reference = HMCExternalReferences()

input_segment_ref = "$0::377894440:$1:801805579#-0.3178966341814717..1"
print('segment_ref', input_segment_ref)
segment_ref_list = input_segment_ref.split(':')
input_partition_name = segment_ref_list[2]
input_segment_id_ref = segment_ref_list[4]
input_segment_id = input_segment_id_ref.split('#')[0]
input_segment_direction = input_segment_id_ref.split('#')[1][0]
input_segment_offset = input_segment_id_ref.split('#')[1][1:]
input_segment_offset_start = input_segment_offset.split('..')[0]
input_segment_offset_end = input_segment_offset.split('..')[1]

input_segment_ref_partition_center = HereQuad.from_long_key(int(input_partition_name)).bounding_box.center
input_segment_ref_partition_center_lat = input_segment_ref_partition_center.lat
input_segment_ref_partition_center_lng = input_segment_ref_partition_center.lng
input_hmc_partition_level_12 = HereQuad.from_lat_lng_level(input_segment_ref_partition_center_lat, input_segment_ref_partition_center_lng,
                                                     12)

external_ref_partition = hmc_external_reference._get_external_references_partition(input_hmc_partition_level_12.long_key)
external_ref_partition_dict = external_ref_partition.to_dict(orient='dict', into=dict)

print(external_ref_partition_dict.keys())

segment_anchor_list = external_ref_partition_dict['segment_anchor'][0]
segment_anchor_index = 0

for segment_anchor in segment_anchor_list:
    first_segment_start_offset = segment_anchor.get('first_segment_start_offset')
    last_segment_end_offset = segment_anchor.get('last_segment_end_offset')
    attribute_orientation = segment_anchor.get('attribute_orientation')
    oriented_segment_ref_list = segment_anchor.get('oriented_segment_ref')

    for oriented_segment_ref in oriented_segment_ref_list:
        segment_ref = oriented_segment_ref.get('segment_ref')
        inverted = oriented_segment_ref.get('inverted')
        partition_name = segment_ref.get('partition_name')
        identifier = segment_ref.get('identifier')

        whole_segment = False

        if input_segment_offset_start == '0' and input_segment_offset_end == '1':
            whole_segment = True

        if input_segment_id == identifier.split(':')[-1]:
            if whole_segment:
                print('identifier', identifier, 'segment_anchor_index', segment_anchor_index)
            else:
                if input_segment_offset_start >= first_segment_start_offset and input_segment_offset_end <= last_segment_end_offset:
                    print('identifier', identifier, 'segment_anchor_index', segment_anchor_index)

    segment_anchor_index += 1
