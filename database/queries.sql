--update gtin code to other items with same product code
UPDATE cfe_item as t1 SET gtin_code=t2.gtin_code 
FROM cfe_item t2 WHERE t2.product_code=t1.product_code 
and t2.gtin_code is not null and t1.gtin_code is null


-- list all gtins missing from product table
select distinct gtin_code from cfe_item
where gtin_code not in (select gtin from cfe_product)
and gtin_code ~ '^[1-9][0-9]{12}$'
order by gtin_code 


-- compare products prices

select * from (
	select gtin_code, description, sum(coop) as coop, sum(sao_roque) as sao_roque, sum(tenda) as tenda, sum(barbosa) as barbosa 
	from (
	-- compare products prices
		with prod as (
		select gtin_code, max(description) as description
		from cfe_item
			where gtin_code is not null
		group by gtin_code
		)

		select distinct i.gtin_code, d.description,

		case 
			when h.place_name ='COOP COOPERATIVA DE CONSUMO' then max(unit_price) 
			else 0
		end as COOP,

		case 
			when h.place_name ='SUPER MERCADO SAO ROQUE LTDA' then max(unit_price) 
			else 0
		end as SAO_ROQUE,

		case 
			when h.place_name ='TENDA ATACADO SA' then max(unit_price) 
			else 0
		end as TENDA,

		case 
			when h.place_name ='SILVA E BARBOSA COMERCIO DE ALIMENTOS LTDA' then max(unit_price) 
			else 0
		end as BARBOSA

		from cfe_item i
		inner join prod d on i.gtin_code = d.gtin_code
		inner join cfe_header h on i.purchase_id = h.id
		group by i.gtin_code, d.description, h.place_name

		) a

	group by gtin_code, description
	)b
	where tenda>0
	
order by description

--CHECK LIQUID PRICE BUG
select * from (
select gtin_code, qtty, gross_price, liquid_price, unit_price, gross_price/qtty as calculado,
case when abs(unit_price -gross_price/qtty) >1 then 'NOK' else 'OK' end as diferenca
from cfe_item
order by gtin_code) x 
where diferenca <>'OK'


select gtin_code, qtty, gross_price, liquid_price, unit_price, gross_price/qtty as calculado,
case when liquid_price<> then 'NOK' else 'OK' end as diferenca
from cfe_item
order by gtin_code

select gtin_code, qtty, gross_price, unit_price, discount, liquid_price, gross_price - discount,
case when abs(liquid_price - (gross_price-discount)) >1 then 'NOK' else 'OK' end as diferenca
from cfe_item
where qtty>1
order by gtin_code

--gross = unit x qtty
--unit = unit price
--liquid = 


-- attempt of calculating consume per day...
with prodfreq as (
select distinct gtin_code, date(h.purchase_date), sum(qtty) as total from cfe_item i
join cfe_header h on i.purchase_id = h.id
group by gtin_code, date(h.purchase_date)
order by gtin_code, date(h.purchase_date)
	)


-- calc consumo
select gtin_code, avg(total/interval) , 1/avg(total/interval) 
from (
	select gtin_code, date, last, date::DATE - last::DATE as interval,total 
	from (
		select gtin_code, date,
		LAG(date,1) OVER (
				PARTITION BY gtin_code
				ORDER BY date
			) as last, 
		total
		from prodfreq) x
		where last is not null) y
	group by gtin_code
--where gtin_code = '0000000008105'

