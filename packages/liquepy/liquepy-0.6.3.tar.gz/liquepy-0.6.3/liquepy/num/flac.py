from sfsimodels import models
import sfsimodels as sm
import numpy as np
from collections import OrderedDict
from sfsimodels.functions import clean_float
from sfsimodels.build_model_descriptions import build_parameter_descriptions
from liquepy.element.models import ShearTest
from liquepy.exceptions import deprecation


class FlacSoil(sm.Soil):
    _tension = 0.0  # default to zero
    hyst_str = ""

    def __str__(self):
        return "Base Soil model, id=%i, phi=%.1f" % (self.id, self.phi)

    def __init__(self, pw=9800, liq_mass_density=None, g=9.8):
        _gravity = g  # m/s2
        if liq_mass_density:
            _liq_mass_density = liq_mass_density  # kg/m3
        elif pw is not None and _gravity is not None:
            if pw == 9800 and g == 9.8:
                _liq_mass_density = 1.0e3
            else:
                _liq_mass_density = pw / _gravity
        else:
            _liq_mass_density = None
        # run parent class initialiser function
        super(FlacSoil, self).__init__(liq_mass_density=_liq_mass_density, g=_gravity)
        self._extra_class_inputs = ["tension"]
        self.inputs = self.inputs + self._extra_class_inputs
        self.flac_parameters = OrderedDict([
            ("bulk", "bulk_mod"),
            ("shear", "g_mod"),
            ("friction", "phi"),
            ("cohesion", "cohesion"),
            ("tension", "tension"),
            ("density", "density"),
            ("dilation", "dilation_angle"),
            ("por", "porosity"),
            ("perm", "flac_permeability")
        ])
        if not hasattr(self, "definitions"):
            self.definitions = OrderedDict()
        self.definitions["density"] = ["Soil mass density", "kg"]
        self.definitions["tension"] = ["Soil strength in tension", "Pa"]
        self.definitions["flac_permeability"] = ["Permeability of soil", "??"]
        self.prop_dict = OrderedDict()

    def set_prop_dict(self):
        plist = []
        for item in self.flac_parameters:
            plist.append(self.flac_parameters[item])
        self.prop_dict = build_parameter_descriptions(self, user_p=self.definitions, output="dict", plist=plist)

    def find_units(self, parameter):
        if parameter in self.prop_dict:
            return self.prop_dict[parameter]["units"]
        else:
            return None

    @property
    def density(self):
        try:
            return self.unit_dry_weight / 9.81
        except TypeError:
            return None

    @property
    def tension(self):
        return self._tension

    @tension.setter
    def tension(self, value):
        value = clean_float(value)
        self._tension = value

    @property
    def flac_permeability(self):
        try:
            return self.permeability / self._pw
        except TypeError:
            return None


class PM4Sand(FlacSoil, sm.StressDependentSoil):
    _h_po = None
    _csr_n15 = None

    _h_o = None  # not required
    n_b = None
    n_d = None
    a_do = None
    z_max = None
    c_z = None
    c_e = None
    g_degr = None
    c_kaf = None
    q_bolt = None
    r_bolt = None
    m_par = None
    mc_ratio = None
    mc_c = None

    # TODO: add non default inputs here
    type = "pm4sand"

    def __init__(self, pw=9800, liq_mass_density=None, g=9.8, p_atm=101000.0, **kwargs):
        # Note: pw has deprecated
        _gravity = g  # m/s2
        if liq_mass_density:
            _liq_mass_density = liq_mass_density  # kg/m3
        elif pw is not None and _gravity is not None:
            if pw == 9800 and g == 9.8:
                _liq_mass_density = 1.0e3
            else:
                _liq_mass_density = pw / _gravity
        else:
            _liq_mass_density = None

        FlacSoil.__init__(self, liq_mass_density=_liq_mass_density, g=_gravity)
        sm.StressDependentSoil.__init__(self, liq_mass_density=_liq_mass_density, g=_gravity, **kwargs)
        self._extra_class_inputs = [
            "hp0",
            "csr_n15",
            "p_atm",
            "h_o",
            "n_b",
            "n_d",
            "a_do",
            "z_max",
            "c_z",
            "c_e",
            "g_degr",
            "c_kaf",
            "q_bolt",
            "r_bolt",
            "m_par",
            "mc_ratio",
            "mc_c"
        ]
        self.p_atm = p_atm
        self.inputs += self._extra_class_inputs
        self.pm4sand_parameters = OrderedDict([
            ("D_r", "relative_density"),
            ("h_po", "h_po"),
            ("G_o", "g0_mod"),
            ("density", "density"),
            ("porosity", "porosity"),
            ("h_o", "h_o"),
            ("e_min", "e_min"),
            ("e_max", "e_max"),
            ("n_b", "n_b"),
            ("n_d", "n_d"),
            ("c_z", "c_z"),
            ("c_e", "c_e"),
            ("n_d", "n_d"),
            ("k11", "flac_permeability"),
            ("k22", "flac_permeability"),
            ("P_atm", "p_atm"),
            ("phi_cv", "phi"),
            ("pois", "poissons_ratio"),
            ("A_do", "a_do"),
            ("G_degr", "g_degr"),
            ("Ckaf", "c_kaf"),
            ("Q_bolt", "q_bolt"),
            ("R_bolt", "r_bolt"),
            ("MC_ratio", "mc_ratio"),
            ("MC_c", "mc_c")
            ])
        if not hasattr(self, "definitions"):
            self.definitions = OrderedDict()
        self.definitions["h_po"] = ["Contraction rate parameter", "-"]
        self.definitions["G_o"] = ["Normalised shear modulus factor", "-"]
        self.definitions["p_atm"] = ["Atmospheric pressure", "Pa"]

    def __repr__(self):
        return "PM4Sand Soil model, id=%i, phi=%.1f, Dr=%.2f" % (self.id, self.phi, self.relative_density)

    def __str__(self):
        return "PM4Sand Soil model, id=%i, phi=%.1f, Dr=%.2f" % (self.id, self.phi, self.relative_density)

    def set_prop_dict(self):
        plist = []
        for item in self.flac_parameters:
            plist.append(self.flac_parameters[item])
        for item in self.pm4sand_parameters:
            plist.append(self.pm4sand_parameters[item])
        self.prop_dict = build_parameter_descriptions(self, user_p=self.definitions, output="dict", plist=plist)

    @property
    def h_po(self):
        return self._h_po

    @h_po.setter
    def h_po(self, value):
        value = clean_float(value)
        self._h_po = value
        if value is not None:
            self._add_to_stack("h_po", value)

    @property
    def hp0(self):
        deprecation('hp0 is deprecated, used h_po')
        return self._h_po

    @hp0.setter
    def hp0(self, value):
        value = clean_float(value)
        self._h_po = value
        if value is not None:
            self._add_to_stack("h_po", value)

    @property
    def csr_n15(self):
        return self._csr_n15

    @csr_n15.setter
    def csr_n15(self, value):
        value = clean_float(value)
        self._csr_n15 = value
        if value is not None:
            self._add_to_stack("h_po", value)

    @property
    def h_o(self):
        """
        Copy description from manual page 79
        :return:
        """
        return self._h_o

    @h_o.setter
    def h_o(self, value):
        self._h_o = value
        if value is not None:
            self._add_to_stack("h_po", value)

    def g_mod_at_v_eff_stress(self, sigma_v_eff):  # Override base function since k0 is different
        return self.get_g_mod_at_v_eff_stress(self, sigma_v_eff)

    def get_g_mod_at_v_eff_stress(self, sigma_v_eff):  # Override base function since k0 is different
        k0 = 1 - np.sin(self.phi_r)
        return self.g0_mod * self.p_atm * (sigma_v_eff * (1 + k0) / 2 / self.p_atm) ** 0.5

    def set_g0_mod_from_g_mod_at_v_eff_stress(self, g_mod, sigma_v_eff):
        k0 = 1 - np.sin(self.phi_r)
        self.g0_mod = g_mod / self.p_atm / (sigma_v_eff * (1 + k0) / 2 / self.p_atm) ** 0.5


    # def e_critical(self, p):
    #     p = float(p)
    #     return self.e_cr0 - self.lamb_crl * np.log(p / self.p_cr0)
    #
    # def dilation_angle(self, p_mean):
    #     critical_relative_density = self._calc_critical_relative_density(p_mean)
    #     xi_r = critical_relative_density - self.relative_density
    #
    # def _calc_critical_relative_density(self, p_mean):
    #     try:
    #         return (self.e_max - self.e_critical(p_mean)) / (self.e_max - self.e_min)
    #     except TypeError:
    #         return None


def load_element_test(ffp, esig_v0, hydrostatic=0):
    ele_data = np.loadtxt(ffp, delimiter="  ", skiprows=1, usecols=(0, 1, 2, 4))
    n_count = ele_data[:, 0]
    csr_vals = ele_data[:, 1]
    tau = csr_vals * esig_v0
    strs = ele_data[:, 2] / 100
    ru_flac = ele_data[:, 3]
    stest = ShearTest(tau, strs, esig_v0=esig_v0, n_cycles=n_count)
    stest.set_pp_via_ru(ru_flac, hydrostatic=hydrostatic)
    stest.set_i_liq(esig_v_limit=5000)
    return stest


def load_file_and_dt(fname):
    num_data_k = np.loadtxt(fname, skiprows=4)
    time = num_data_k[:, 0]  # This get the first column
    dt = time[1] - time[0]
    values = num_data_k[:, 1]
    return values, dt


def load_file_and_time(fname):
    num_data_k = np.loadtxt(fname, skiprows=4)
    time = num_data_k[:, 0]  # This get the first column
    values = num_data_k[:, 1]
    return values, time


def load_input_motion_and_dt(ffp):
    """
    Loads acceleration values and time step that were saved in FLAC input format.

    Parameters
    ----------
    ffp: str
        Full file path to output file

    Returns
    -------
    values: array_like
        An array of values
    dt: float
        Time step

    """
    data = np.genfromtxt(ffp, skip_header=1, delimiter=",", names=True, usecols=0)
    dt = data.dtype.names[0].split("_")[-1]
    dt = "." + dt[1:]
    dt = float(dt)
    acc = data.astype(np.float)
    return acc, dt


def save_input_motion_and_dt(ffp, values, dt, label="unlabelled"):
    """
    Exports acceleration values to the FLAC input format.

    Parameters
    ----------
    ffp: str
        Full file path to output file
    values: array_like
        An array of values
    dt: float
        Time step
    label: str
        A label of the data

    Returns
    -------

    """
    para = [label, "%i %.4f" % (len(values), dt)]
    for i in range(len(values)):
        para.append("%.6f" % values[i])
    ofile = open(ffp, "w")
    ofile.write("\n".join(para))
    ofile.close()


def save_input_motion(ffp, name, values, dt):
    """
    Exports acceleration values to the FLAC input format.

    :param ffp: str, full file path to output file
    :param name: str, name of records
    :param values: array, acceleration values
    :param dt: float, time step
    :return: None
    """
    deprecation("liquepy.num.flac.save_input_motion is deprecated, use liquepy.num.flac.save_input_motion_and_dt")
    para = [name, "%i %.4f" % (len(values), dt)]
    for i in range(len(values)):
        para.append("%.6f" % values[i])
    ofile = open(ffp, "w")
    ofile.write("\n".join(para))
    ofile.close()


def calc_hp0_from_crr_n15_and_relative_density_millen_et_al_2019(crr_n15, d_r):
    return crr_n15 * (2.05 - 2.4 * d_r) / (1. - crr_n15 * (12.0 - (12.5 * d_r)))
