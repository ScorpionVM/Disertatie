from math import cos, sin, degrees, radians

g = 9.80665

tetha_g = radians(90)
tetha_b = radians(90)
tetha_w = radians(0)

# Gravity
Fg = m_g * m_v * m_p

Fxg = Fg * cos(tetha_g)
Fyg = Fg * sin(tetha_g)

# Buoyancy
Fb = (rho_a - rho_g)*g*V

Fxb = Fb * cos(tetha_b)
Fyb = Fb * cos(tetha_b)

# Wind
# m_w - masa vantului
# v_w - viteza vantului
# t_w - durata

Fw = m_w * v_w/t_w

Fxw = Fw * cos(tetha_w)
Fyw = Fw * sin(tetha_w)

# Total Forces
Fxt = Fxg + Fxb + Fxw
Fyt = Fyg + Fyb + Fyw

# Resultant Angle
# tan(tetha_r) = Fyt / Fxt

# Resultant Force
# Fxt = Fr * cos(tetha_r)
# Fyt = Fr * sin(tetha_r)


