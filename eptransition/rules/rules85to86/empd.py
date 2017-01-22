import math

from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):  # pragma no cover
    def saturation_press(self, t_db):
        """
        Function to compute saturation vapor pressure in [kPa]
        ASHRAE Fundamentals handbood (2005) p 6.2, equation 5 and 6

        Valid from -100C to 200 C

        :param t_db: Dry bulb temperature [degC]
        :return: Saturation pressure
        """
        c1 = -5674.5359
        c2 = 6.3925247
        c3 = -0.009677843
        c4 = 0.00000062215701
        c5 = 2.0747825E-09
        c6 = -9.484024E-13
        c7 = 4.1635019
        c8 = -5800.2206
        c9 = 1.3914993
        c10 = -0.048640239
        c11 = 0.000041764768
        c12 = -0.000000014452093
        c13 = 6.5459673

        t_k = t_db + 273.15  # converts from degC to degK

        if t_k <= 273.15:
            result = math.exp(c1 / t_k + c2 + c3 * t_k + c4 * t_k ** 2 + c5 * t_k ** 3 +
                              c6 * t_k ** 4 + c7 * math.log(t_k)) / 1000
        else:
            result = math.exp(c8 / t_k + c9 + c10 * t_k + c11 * t_k ** 2 + c12 * t_k ** 3 +
                              c13 * math.log(t_k)) / 1000
        return result

    def calculate_mu_empd(self, d_empd, a, b, c, d, density_matl):
        """
        Calculate the mu_EMPD parameter given EPMD inputs from an 8.4.0 example file.

        :param d_empd: original N1 field
        :param a: original N2 field
        :param b: original N3 field
        :param c: original N4 field
        :param d: original N5 field
        :param density_matl: density of the material, looked up from the Material object.
        :return: A new value for the F2 field, mu_empd
        """

        # Assume T, RH, and P
        temperature = 24  # degC
        relative_humidity = 0.45
        ambient_pressure = 101325

        # Assume time interval of 24 hours
        t_p = 24 * 60 * 60  # seconds

        slope__m_c = a * b * relative_humidity ** (b - 1) + c * d * relative_humidity ** (d - 1)
        p_v_sat = self.saturation_press(temperature) * 1000  # kPa -> Pa

        diffusivity_empd = d_empd ** 2 * math.pi * slope__m_c * density_matl / (t_p * p_v_sat)

        diffusivity_air = 2.0e-7 * (temperature + 273.15) ** 0.81 / ambient_pressure

        return diffusivity_air / diffusivity_empd

    def get_name_of_object_to_transition(self):
        return "MaterialProperty:MoisturePenetrationDepth:Settings"

    def get_names_of_dependent_objects(self):
        return ["Material"]

    def transition(self, core_object, dependent_objects):  # pragma no cover
        original_idf_fields = core_object.fields
        new_idf_fields = [original_idf_fields[0]]
        old_field_2 = original_idf_fields[1]
        old_d_empd = float(original_idf_fields[1])
        old_a = float(original_idf_fields[2])
        old_b = float(original_idf_fields[3])
        old_c = float(original_idf_fields[4])
        old_d = float(original_idf_fields[5])
        empd_material_name = original_idf_fields[0]
        material = [x for x in dependent_objects["MATERIAL"] if x.fields[0].upper() == empd_material_name.upper()][0]
        old_density_material = float(material.fields[4])
        new_mu = self.calculate_mu_empd(old_d_empd, old_a, old_b, old_c, old_d, old_density_material)
        new_idf_fields.append(str(new_mu))
        new_idf_fields.extend(original_idf_fields[2:6])
        new_idf_fields.append(old_field_2)
        new_idf_fields.extend(["0.0"] * 3)
        new_empd_object = IDFObject([core_object.object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        return TransitionReturn([new_empd_object])
