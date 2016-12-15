Tribute


total mortgage out, taking lower band, so understated.


select a.region_id::int as id,  d.the_geom, (
m_1_299_tot*1 + 
m_300_449_tot*300 +
m_450_599_tot*240 +
m_600_799_tot*600 +
m_800_999_tot*800 +
m_1000_1399_tot*1000 + 
m_1400_1799_tot*1400 +
m_1800_2399_tot*1800 +
m_2400_2999_tot*2400 +
m_3000_3999_tot*3000 +
m_4000_over_tot*4000)::int as total_mortgage_out,
(p_1_199_tot*1 + 
p_200_299_tot*200 +
p_300_399_tot*300 +
p_400_599_tot*400 + 
p_600_799_tot*600 +
p_800_999_tot*800 + 
p_1000_1249_tot*1000 +
p_1250_1499_tot*1250 +
p_1500_1999_tot*1500 +
p_2000_more_tot*2000)::int as total_wage_in,
Tot_Tot::int as total_workers,
fin_and_ins_s_tot::int as fin_sector_workers
from a2011census_b33_nsw_sa1_short as a join a2011census_b17b_nsw_sa1_short as b on a.region_id = b.region_id join a2011census_b44a_nsw_sa1_short as c on a.region_id = c.region_id join abs_sa1_2011 as d on a.region_id::int = d.region_id::int;