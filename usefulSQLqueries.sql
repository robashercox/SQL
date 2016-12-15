-- query to update attribute based on spatial join 
update oppSites set old_zoning = existing.zoning from 
(
select oppSites.id as id , zoning_existing.sym_code as zoning from zoning_existing, oppSites where st_within(st_centroid(oppSites.geom), zoning_existing.geom)
) existing
where existing.id = oppSites.id;

-- classic spatial join
select syd_cadastre.*,r1r2r3ru5.sym_code from syd_cadastre, r1r2r3ru5 where st_within (st_centroid(syd_cadastre.geom), r1r2r3ru5.geom);


-- query that joins 3 tables on transport code BTS
select tz_nsw_2011.geom, tz_nsw_2011.tz_code11::int, (pop.pop/st_area(tz_nsw_2011.geom)) as pop, (emp.emp/st_area(tz_nsw_2011.geom)) as emp from 
tz_nsw_2011 join 
(
select tz11, sum(emp) as emp from abts_employment_forecasts_dataset_2011_2041 where year = 2011 group by tz11
) as emp
on tz_nsw_2011.tz_code11 = emp.tz11 join
(
select tz11, sum(erp) as pop from abts_population_forecasts_erp_opd_2011_2041 where year = 2011 group by tz11
) as pop
on tz_nsw_2011.tz_code11 = pop.tz11


--- make web geojson

select a.geom, a.sa1_7digit::int, round(a.station_dist::double precision,3) as station_dist, 
b.median_age_persons::int as median_age,b.median_mortgage_repay_monthly::int as mort_repay,b.median_rent_weekly::int as median_rent,
b.median_tot_fam_inc_weekly::int as median_fam_income,round(b.average_num_psns_per_bedroom,2) as pers_per_bedr,round(b.average_household_size) as av_hh_size 
from smallsyd as a join  a2011census_b02_nsw_sa1_short as b on a.sa1_7digit::int= b.region_id::int


select e.o_sa2_11, array_agg(e.dest) from (select d.o_sa2_11, array[d.d_sa2_11::text, mode15::text, mode15_name::text, sum::text] as dest  from (select o_sa2_11::int, d_sa2_11::int, mode15::int, mode15_name, sum(employed_persons) 
from ajtwmodesa2 where substring(o_sa2_11::text from 1 for 2)::int = 11 
group by o_sa2_11, d_sa2_11, mode15,mode15_name) as d) as e group by e.o_sa2_11

-- classify transport from JTW
(select o_sa2_11::int, d_sa2_11::int, sum (case
when (mode15_name = 'Train') 
or (mode15_name = 'Bus')
or (mode15_name = 'Tram')
or (mode15_name = 'Ferry') then employed_persons else 0 end)::int as public,
sum(case
when (mode15_name = 'Car as driver') 
or (mode15_name = 'Car as passenger')
or (mode15_name = 'Taxi')
or (mode15_name = 'Truck')
or (mode15_name = 'Motorbike') then employed_persons else 0 end)::int as private,
sum(case
when (mode15_name = 'Walked only') 
or (mode15_name = 'bicycle') then employed_persons else 0 end)::int as foot,
sum(case 
when (mode15_name = 'Did not go to work')
or  (mode15_name = 'Worked at home') then employed_persons else 0 end)::int as stayed
from ajtwmodesa2
group by o_sa2_11, d_sa2_11)

--- get median

with ordered as (select %s::int, row_number() over (order by %s) as row_id,
		(Select count(1) from abs_sa1_2011) as ct
		from abs_sa1_2011 order by row_id )
		select avg(%s)::int as median from ordered where row_id between ct/2.0 and ct/2.0+1