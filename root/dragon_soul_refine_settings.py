import item

default_grade_need_count = [2, 2, 2, 2]
default_grade_fee = [50000, 100000, 250000, 1500000]
default_grade_percent = [85, 75, 60, 40]

default_step_need_count = [2, 2, 2, 2, 2]
default_step_fee = [500000, 1000000, 5000000, 20000000, 50000000]
default_step_percent = [85, 70, 55, 40, 100]

strength_fee = {
	item.MATERIAL_DS_REFINE_NORMAL : 1000000,
	item.MATERIAL_DS_REFINE_BLESSED : 1500000,
	item.MATERIAL_DS_REFINE_HOLLY : 3000000,
}

default_strength_max_table = [
	[2, 2, 3, 3, 4],
	[3, 3, 3, 4, 4],
	[4, 4, 4, 4, 4],
	[4, 4, 4, 4, 5],
	[4, 4, 4, 5, 6],
]

STRENGTH_PERCENTS = {
	item.MATERIAL_DS_REFINE_NORMAL : [70, 60, 50, 40, 30, 20],
	item.MATERIAL_DS_REFINE_BLESSED : [75, 65, 55, 45, 35, 25],
	item.MATERIAL_DS_REFINE_HOLLY : [80, 70, 60, 50, 40, 30],
}

default_refine_info = {
	"grade_need_count" : default_grade_need_count,
	"grade_fee" : default_grade_fee,
	"grade_percent" : default_grade_percent,
	"step_need_count" : default_step_need_count,
	"step_fee" : default_step_fee,
	"step_percent" : default_step_percent,
	"strength_max_table" : default_strength_max_table,
}

dragon_soul_refine_info = {
	11 : default_refine_info,
	12 : default_refine_info,
	13 : default_refine_info,
	14 : default_refine_info,
	15 : default_refine_info,
	16 : default_refine_info,
}
