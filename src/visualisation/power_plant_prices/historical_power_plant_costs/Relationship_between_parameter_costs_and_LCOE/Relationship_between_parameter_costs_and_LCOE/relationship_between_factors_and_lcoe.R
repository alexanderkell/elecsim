pre_development = c(10000, 12000, 14000, 16000, 18000, 20000, 22000, 24000, 26000)
construction = c(500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000)
infrastructure = c(15100000, 18120000, 21140000)
fixed_om = c(12200, 14640, 17080)
var_om = c(3, 3.6, 4.2)
insurance = c(2100, 2520, 2940)
connection = c(3300, 3960, 4620)
LCOE = c(48.82, 50.75, 52.68, 54.61, 56.53, 58.46, 60.39, 62.32, 64.24)
diff(LCOE)
x = c(1,2,3)

data = data.frame(pre_development, construction, infrastructure, fixed_om, var_om, insurance, connection, LCOE)

plot(x,LCOE)

abline(lm(LCOE~x))

fit = lm(LCOE~pre_development+construction+infrastructure+fixed_om+var_om+insurance+connection, data=data)
fit
