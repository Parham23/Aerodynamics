
import math

# ==========================================================
# ANDERSON AERODYNAMICS TOOLBOX
# PROTOTYPE 2: INTERACTIVE CALCULATION ENGINE
# ==========================================================

GAMMA_DEFAULT = 1.4
R_DEFAULT = 287.0


# ==========================================================
# 1. UNIT SYSTEM
# All calculations internally use SI units
# ==========================================================

UNITS = {
    "pressure": {
        "Pa": 1.0,
        "kPa": 1000.0,
        "MPa": 1e6,
        "atm": 101325.0,
        "bar": 100000.0,
        "psi": 6894.757293,
        "psf": 47.88025898
    },

    "velocity": {
        "m/s": 1.0,
        "km/h": 1 / 3.6,
        "ft/s": 0.3048,
        "mph": 0.44704
    },

    "density": {
        "kg/m^3": 1.0,
        "g/cm^3": 1000.0,
        "slug/ft^3": 515.3788184,
        "lbm/ft^3": 16.01846337
    },

    "temperature": ["K", "C", "F", "R"],

    "specific_heat": {
        "J/(kg.K)": 1.0,
        "kJ/(kg.K)": 1000.0,
        "BTU/(lbm.R)": 4186.8
    },

    "specific_energy": {
        "J/kg": 1.0,
        "kJ/kg": 1000.0,
        "BTU/lbm": 2326.0
    },
    "specific_entropy": {
    "J/(kg.K)": 1.0,
    "kJ/(kg.K)": 1000.0,
    "BTU/(lbm.R)": 4186.8
    },


}


def to_si(value, quantity, unit):

    if quantity == "temperature":

        if unit == "K":
            return value

        elif unit == "C":
            return value + 273.15

        elif unit == "F":
            return (value - 32) * 5 / 9 + 273.15

        elif unit == "R":
            return value * 5 / 9

    else:
        return value * UNITS[quantity][unit]


def from_si(value, quantity, unit):

    if quantity == "temperature":

        if unit == "K":
            return value

        elif unit == "C":
            return value - 273.15

        elif unit == "F":
            return (value - 273.15) * 9 / 5 + 32

        elif unit == "R":
            return value * 9 / 5

    else:
        return value / UNITS[quantity][unit]


# ==========================================================
# 2. TERMINAL INPUT FUNCTIONS
# ==========================================================

def get_number(message):

    while True:
        try:
            return float(input(message))

        except ValueError:
            print("Please enter a valid number.")


def get_unit(quantity):

    available = UNITS[quantity]

    if quantity == "temperature":
        units = available
    else:
        units = list(available.keys())

    print("\nAvailable units:")
    for unit in units:
        print(f"  {unit}")

    while True:
        unit = input("Select unit: ").strip()

        if unit in units:
            return unit

        print("Invalid unit. Try again.")


def get_property(name, quantity):

    value = get_number(f"Enter {name}: ")
    unit = get_unit(quantity)

    return to_si(value, quantity, unit)


def display_result(name, value, quantity):

    print(f"\nAvailable output units:")

    available = UNITS[quantity]

    if quantity == "temperature":
        units = available
    else:
        units = list(available.keys())

    for unit in units:
        print(f"  {unit}")

    while True:
        unit = input("Desired output unit: ").strip()

        if unit in units:
            break

        print("Invalid unit. Try again.")

    result = from_si(value, quantity, unit)

    print("\n========================================")
    print("FINAL RESULT")
    print("========================================")
    print(f"{name} = {result:.8f} {unit}")



def get_gamma():

    value = input(
        f"Specific heat ratio gamma [{GAMMA_DEFAULT}]: "
    ).strip()

    if value == "":
        return GAMMA_DEFAULT

    gamma = float(value)

    if gamma <= 1:
        raise ValueError("Gamma must be greater than 1.")

    return gamma



# ==========================================================
# 3. SOLUTION DISPLAY
# ==========================================================

def show_solution(given, unknown, equation_steps):

    print("\n========================================")
    print("GIVEN VARIABLES")
    print("========================================")

    for name, value, unit in given:
        print(f"{name} = {value:.8f} {unit}")

    print("\n========================================")
    print("UNKNOWN VARIABLE")
    print("========================================")

    print(unknown)

    print("\n========================================")
    print("STEP-BY-STEP SOLUTION")
    print("========================================")

    for step in equation_steps:
        print(step)


# ==========================================================
# 4. IDEAL GAS EQUATION
# p = rho * R * T
# ==========================================================

def ideal_gas():

    print("\n========== IDEAL GAS EQUATION ==========")
    print("Equation: p = rho * R * T")

    print("\nSelect unknown:")
    print("[1] Pressure (p)")
    print("[2] Density (rho)")
    print("[3] Temperature (T)")

    choice = input("Your choice: ")

    if choice not in ("1", "2", "3"):
        print("Invalid selection.")
        return

    unknowns = {
        "1": ("Pressure", "pressure", "p"),
        "2": ("Density", "density", "rho"),
        "3": ("Temperature", "temperature", "T")
    }

    name, quantity, symbol = unknowns[choice]

    R = get_number(
        f"Specific gas constant R [{R_DEFAULT}]: "
    )

    if R == 0:
        R = R_DEFAULT

    if R <= 0:
        print("R must be positive.")
        return

    given = []
    steps = []

    try:

        if symbol == "p":

            rho = get_property("Density", "density")
            T = get_property("Temperature", "temperature")

            if rho <= 0 or T <= 0:
                raise ValueError("Density and temperature must be positive.")

            result = rho * R * T

            given = [
                ("Density", rho, "kg/m^3"),
                ("Temperature", T, "K"),
                ("R", R, "J/(kg.K)")
            ]

            steps = [
                "Governing equation: p = rho * R * T",
                f"p = {rho:.8f} * {R:.8f} * {T:.8f}",
                f"p = {result:.8f} Pa"
            ]

        elif symbol == "rho":

            p = get_property("Pressure", "pressure")
            T = get_property("Temperature", "temperature")

            if p <= 0 or T <= 0:
                raise ValueError("Pressure and temperature must be positive.")

            result = p / (R * T)

            given = [
                ("Pressure", p, "Pa"),
                ("Temperature", T, "K"),
                ("R", R, "J/(kg.K)")
            ]

            steps = [
                "Governing equation: p = rho * R * T",
                "Rearrange: rho = p / (R * T)",
                f"rho = {p:.8f} / ({R:.8f} * {T:.8f})",
                f"rho = {result:.8f} kg/m^3"
            ]

        else:

            p = get_property("Pressure", "pressure")
            rho = get_property("Density", "density")

            if p <= 0 or rho <= 0:
                raise ValueError("Pressure and density must be positive.")

            result = p / (rho * R)

            given = [
                ("Pressure", p, "Pa"),
                ("Density", rho, "kg/m^3"),
                ("R", R, "J/(kg.K)")
            ]

            steps = [
                "Governing equation: p = rho * R * T",
                "Rearrange: T = p / (rho * R)",
                f"T = {p:.8f} / ({rho:.8f} * {R:.8f})",
                f"T = {result:.8f} K"
            ]

        if not math.isfinite(result) or result <= 0:
            raise ValueError("Calculated result is not physically valid.")

        show_solution(given, name, steps)
        display_result(name, result, quantity)

    except (ValueError, KeyError) as error:
        print(f"\nCalculation error: {error}")


# ==========================================================
# 5. MACH NUMBER RELATION
# M = V / a
# ==========================================================

def mach_calculator():

    print("\n========== MACH NUMBER ==========")
    print("Equation: M = V / a")

    print("\nSelect unknown:")
    print("[1] Mach number (M)")
    print("[2] Velocity (V)")
    print("[3] Speed of sound (a)")

    choice = input("Your choice: ")

    if choice not in ("1", "2", "3"):
        print("Invalid selection.")
        return

    try:

        given = []
        steps = []

        if choice == "1":

            V = get_property("Velocity", "velocity")
            a = get_property("Speed of sound", "velocity")

            if V < 0 or a <= 0:
                raise ValueError("Invalid velocity or sound speed.")

            result = V / a

            given = [
                ("Velocity", V, "m/s"),
                ("Speed of sound", a, "m/s")
            ]

            steps = [
                "Governing equation: M = V / a",
                f"M = {V:.8f} / {a:.8f}",
                f"M = {result:.8f}"
            ]

            show_solution(given, "Mach number (M)", steps)

            print(f"\nMach number = {result:.8f}")
            print(f"Flow classification = {classify_flow(result)}")

        elif choice == "2":

            M = get_number("Enter Mach number: ")
            a = get_property("Speed of sound", "velocity")

            if M < 0 or a <= 0:
                raise ValueError("Invalid Mach number or sound speed.")

            result = M * a

            given = [
                ("Mach number", M, ""),
                ("Speed of sound", a, "m/s")
            ]

            steps = [
                "Governing equation: M = V / a",
                "Rearrange: V = M * a",
                f"V = {M:.8f} * {a:.8f}",
                f"V = {result:.8f} m/s"
            ]

            show_solution(given, "Velocity (V)", steps)
            display_result("Velocity", result, "velocity")

        else:

            M = get_number("Enter Mach number: ")
            V = get_property("Velocity", "velocity")

            if M <= 0 or V < 0:
                raise ValueError("Invalid Mach number or velocity.")

            result = V / M

            given = [
                ("Mach number", M, ""),
                ("Velocity", V, "m/s")
            ]

            steps = [
                "Governing equation: M = V / a",
                "Rearrange: a = V / M",
                f"a = {V:.8f} / {M:.8f}",
                f"a = {result:.8f} m/s"
            ]

            show_solution(given, "Speed of sound (a)", steps)
            display_result("Speed of sound", result, "velocity")

    except (ValueError, KeyError) as error:
        print(f"\nCalculation error: {error}")


# ==========================================================
# 5.1 THERMODYNAMIC PROPERTIES
# Cp, Cv, R, gamma, enthalpy and internal energy
# ==========================================================


def thermodynamic_properties():

    print("\n========== THERMODYNAMIC PROPERTIES ==========")

    print("[1] Calculate Cp from Cv and R")
    print("[2] Calculate Cv from Cp and R")
    print("[3] Calculate R from Cp and Cv")
    print("[4] Calculate gamma from Cp and Cv")
    print("[5] Calculate BOTH Cp and Cv from R and gamma")

    choice = input("\nSelect unknown: ")

    if choice not in ("1", "2", "3", "4", "5"):
        print("Invalid selection.")
        return

    try:

        if choice == "1":

            Cv = get_property("Cv", "specific_heat")
            R = get_property("R", "specific_heat")

            if Cv <= 0 or R <= 0:
                raise ValueError("Inputs must be positive.")

            result = Cv + R
            name = "Cp"
            equation = "Cp = Cv + R"

        elif choice == "2":

            Cp = get_property("Cp", "specific_heat")
            R = get_property("R", "specific_heat")

            if Cp <= R or R <= 0:
                raise ValueError("Cp must be greater than R.")

            result = Cp - R
            name = "Cv"
            equation = "Cv = Cp - R"

        elif choice == "3":

            Cp = get_property("Cp", "specific_heat")
            Cv = get_property("Cv", "specific_heat")

            if Cp <= Cv or Cv <= 0:
                raise ValueError("Cp must be greater than Cv.")

            result = Cp - Cv
            name = "R"
            equation = "R = Cp - Cv"

        elif choice == "4":

            Cp = get_property("Cp", "specific_heat")
            Cv = get_property("Cv", "specific_heat")

            if Cp <= Cv or Cv <= 0:
                raise ValueError("Cp must be greater than Cv.")

            result = Cp / Cv
            name = "gamma"
            equation = "gamma = Cp / Cv"

        else:

            R = get_property("R", "specific_heat")
            gamma = get_number("Specific heat ratio gamma: ")

            if R <= 0 or gamma <= 1:
                raise ValueError("R must be positive and gamma > 1.")

            Cv = R / (gamma - 1)
            Cp = gamma * R / (gamma - 1)

            print("\nGIVEN VARIABLES")
            print(f"R = {R:.8f} J/(kg.K)")
            print(f"gamma = {gamma:.8f}")

            print("\nSTEP 1: Calculate Cv")
            print("Cv = R / (gamma - 1)")
            print(f"Cv = {R:.8f} / ({gamma:.8f} - 1)")
            print(f"Cv = {Cv:.8f} J/(kg.K)")

            print("\nSTEP 2: Calculate Cp")
            print("Cp = gamma * R / (gamma - 1)")
            print(f"Cp = {gamma:.8f} * {R:.8f} / ({gamma:.8f} - 1)")
            print(f"Cp = {Cp:.8f} J/(kg.K)")

            print("\nFINAL RESULTS")

            display_result("Cv", Cv, "specific_heat")
            display_result("Cp", Cp, "specific_heat")

            return

        print("\nGIVEN VARIABLES")

        if choice == "1":
            print(f"Cv = {Cv:.8f} J/(kg.K)")
            print(f"R = {R:.8f} J/(kg.K)")

        elif choice == "2":
            print(f"Cp = {Cp:.8f} J/(kg.K)")
            print(f"R = {R:.8f} J/(kg.K)")

        else:
            print(f"Cp = {Cp:.8f} J/(kg.K)")
            print(f"Cv = {Cv:.8f} J/(kg.K)")

        print(f"\nUNKNOWN: {name}")
        print("\nSTEP-BY-STEP SOLUTION")
        print(f"Equation: {equation}")

        if choice == "1":
            print(f"Cp = {Cv:.8f} + {R:.8f}")
        elif choice == "2":
            print(f"Cv = {Cp:.8f} - {R:.8f}")
        elif choice == "3":
            print(f"R = {Cp:.8f} - {Cv:.8f}")
        else:
            print(f"gamma = {Cp:.8f} / {Cv:.8f}")

        print(f"Result = {result:.8f}")

        if name == "gamma":
            print(f"\nSpecific heat ratio = {result:.8f}")
        else:
            display_result(name, result, "specific_heat")

    except (ValueError, KeyError) as error:
        print(f"\nCalculation error: {error}")


# ==========================================================
# 5.2 ENTHALPY AND INTERNAL ENERGY
# ==========================================================

def energy_properties():

    print("\n========== ENTHALPY & INTERNAL ENERGY ==========")

    print("[1] Enthalpy (h)")
    print("[2] Internal energy (e)")

    choice = input("Select property: ")

    if choice not in ("1", "2"):
        print("Invalid selection.")
        return

    if choice == "1":
        name = "Enthalpy"
        symbol = "h"
        heat_name = "Cp"
        quantity = "specific_heat"
    else:
        name = "Internal energy"
        symbol = "e"
        heat_name = "Cv"
        quantity = "specific_heat"

    print(f"\nCalculate {name}")
    print("[1] Absolute property: h = Cp*T or e = Cv*T")
    print("[2] Property change: delta h = Cp*(T2-T1)")
    print("    or delta e = Cv*(T2-T1)")

    mode = input("Select calculation: ")

    if mode not in ("1", "2"):
        print("Invalid selection.")
        return

    try:

        heat = get_property(heat_name, quantity)

        if heat <= 0:
            raise ValueError("Specific heat must be positive.")

        if mode == "1":

            T = get_property("Temperature", "temperature")

            if T <= 0:
                raise ValueError("Temperature must be positive.")

            result = heat * T

            equation = f"{symbol} = {heat_name} * T"
            substitution = (
                f"{symbol} = {heat:.8f} * {T:.8f}"
            )

            print("\nGIVEN VARIABLES")
            print(f"{heat_name} = {heat:.8f} J/(kg.K)")
            print(f"T = {T:.8f} K")

            unknown = name

        else:

            T1 = get_property("Initial temperature T1", "temperature")
            T2 = get_property("Final temperature T2", "temperature")

            if T1 <= 0 or T2 <= 0:
                raise ValueError("Temperatures must be positive.")

            delta_T = T2 - T1
            result = heat * delta_T

            equation = f"Delta {symbol} = {heat_name} * (T2-T1)"
            substitution = (
                f"Delta {symbol} = {heat:.8f} * "
                f"({T2:.8f} - {T1:.8f})"
            )

            print("\nGIVEN VARIABLES")
            print(f"{heat_name} = {heat:.8f} J/(kg.K)")
            print(f"T1 = {T1:.8f} K")
            print(f"T2 = {T2:.8f} K")
            print(f"Delta T = {delta_T:.8f} K")

            unknown = f"Change in {name}"

        print("\nSTEP-BY-STEP SOLUTION")
        print(f"Equation: {equation}")
        print(substitution)
        print(f"Result = {result:.8f} J/kg")

        display_result(name, result, "specific_energy")

    except (ValueError, KeyError) as error:
        print(f"\nCalculation error: {error}")
# ==========================================================
# 5.3 Entropy
# 
# ==========================================================

def entropy_change():
    print("\n--- SPECIFIC ENTROPY CHANGE ---")
    print("Choose the equation you want to use:")
    print("[1] Using temperature and pressure")
    print("[2] Using temperature and density")
    print("[3] Using ratios directly")

    method = input("Select method: ").strip()

    if method == "1":
        print("\nEquation:")
        print("Delta_s = Cp * ln(T2/T1) - R * ln(p2/p1)")

        T1 = get_property("Initial temperature T1", "temperature")
        T2 = get_property("Final temperature T2", "temperature")
        p1 = get_property("Initial pressure p1", "pressure")
        p2 = get_property("Final pressure p2", "pressure")
        Cp = get_property("Specific heat Cp", "specific_heat")
        R = get_property("Specific gas constant R", "specific_heat")

        if min(T1, T2, p1, p2, Cp, R) <= 0:
            print("Error: All inputs must be positive.")
            return

        delta_s = Cp * math.log(T2 / T1) - R * math.log(p2 / p1)

        given = [
            ("Initial temperature T1", T1, "K"),
            ("Final temperature T2", T2, "K"),
            ("Initial pressure p1", p1, "Pa"),
            ("Final pressure p2", p2, "Pa"),
            ("Specific heat Cp", Cp, "J/(kg.K)"),
            ("Specific gas constant R", R, "J/(kg.K)")
        ]

        equation_steps = [
            "STEP 1: Governing equation",
            "Delta_s = Cp * ln(T2/T1) - R * ln(p2/p1)",

            "STEP 2: Substitute the known values",
            f"Delta_s = {Cp:.4f} * ln({T2:.4f}/{T1:.4f})"
            f" - {R:.4f} * ln({p2:.4f}/{p1:.4f})",

            "STEP 3: Calculate the ratios",
            f"T2/T1 = {T2/T1:.6f}",
            f"p2/p1 = {p2/p1:.6f}",

            "STEP 4: Calculate the logarithms",
            f"ln(T2/T1) = {math.log(T2/T1):.6f}",
            f"ln(p2/p1) = {math.log(p2/p1):.6f}",

            "STEP 5: Calculate each term",
            f"Cp * ln(T2/T1) = {Cp * math.log(T2/T1):.4f}",
            f"R * ln(p2/p1) = {R * math.log(p2/p1):.4f}",

            "STEP 6: Final result",
            f"Delta_s = {delta_s:.4f} J/(kg.K)"
        ]

    elif method == "2":
        print("\nEquation:")
        print("Delta_s = Cv * ln(T2/T1) + R * ln(rho2/rho1)")

        T1 = get_property("Initial temperature T1", "temperature")
        T2 = get_property("Final temperature T2", "temperature")
        rho1 = get_property("Initial density rho1", "density")
        rho2 = get_property("Final density rho2", "density")
        Cv = get_property("Specific heat Cv", "specific_heat")
        R = get_property("Specific gas constant R", "specific_heat")

        if min(T1, T2, rho1, rho2, Cv, R) <= 0:
            print("Error: All inputs must be positive.")
            return

        delta_s = Cv * math.log(T2 / T1) + R * math.log(rho2 / rho1)

        given = [
            ("Initial temperature T1", T1, "K"),
            ("Final temperature T2", T2, "K"),
            ("Initial density rho1", rho1, "kg/m^3"),
            ("Final density rho2", rho2, "kg/m^3"),
            ("Specific heat Cv", Cv, "J/(kg.K)"),
            ("Specific gas constant R", R, "J/(kg.K)")
        ]

        equation_steps = [
            "STEP 1: Governing equation",
            "Delta_s = Cv * ln(T2/T1) + R * ln(rho2/rho1)",

            "STEP 2: Substitute the known values",
            f"Delta_s = {Cv:.4f} * ln({T2:.4f}/{T1:.4f})"
            f" + {R:.4f} * ln({rho2:.4f}/{rho1:.4f})",

            "STEP 3: Calculate the ratios",
            f"T2/T1 = {T2/T1:.6f}",
            f"rho2/rho1 = {rho2/rho1:.6f}",

            "STEP 4: Calculate the logarithms",
            f"ln(T2/T1) = {math.log(T2/T1):.6f}",
            f"ln(rho2/rho1) = {math.log(rho2/rho1):.6f}",

            "STEP 5: Calculate each term",
            f"Cv * ln(T2/T1) = {Cv * math.log(T2/T1):.4f}",
            f"R * ln(rho2/rho1) = {R * math.log(rho2/rho1):.4f}",

            "STEP 6: Final result",
            f"Delta_s = {delta_s:.4f} J/(kg.K)"
        ]

    elif method == "3":
        print("\nChoose the available ratios:")
        print("[1] Temperature ratio and pressure ratio")
        print("[2] Temperature ratio and density ratio")

        ratio_method = input("Select method: ").strip()

        T_ratio = get_number("Enter temperature ratio T2/T1: ")

        if T_ratio <= 0:
            print("Error: Ratios must be positive.")
            return

        if ratio_method == "1":
            p_ratio = get_number("Enter pressure ratio p2/p1: ")

            if p_ratio <= 0:
                print("Error: Ratios must be positive.")
                return

            Cp = get_property("Specific heat Cp", "specific_heat")
            R = get_property("Specific gas constant R", "specific_heat")

            if Cp <= 0 or R <= 0:
                print("Error: Cp and R must be positive.")
                return

            term1 = Cp * math.log(T_ratio)
            term2 = R * math.log(p_ratio)
            delta_s = term1 - term2

            given = [
                ("Temperature ratio T2/T1", T_ratio, "dimensionless"),
                ("Pressure ratio p2/p1", p_ratio, "dimensionless"),
                ("Specific heat Cp", Cp, "J/(kg.K)"),
                ("Specific gas constant R", R, "J/(kg.K)")
            ]

            equation_steps = [
                "STEP 1: Governing equation",
                "Delta_s = Cp * ln(T2/T1) - R * ln(p2/p1)",

                "STEP 2: Substitute the given ratios",
                f"Delta_s = {Cp:.4f} * ln({T_ratio:.6f})"
                f" - {R:.4f} * ln({p_ratio:.6f})",

                "STEP 3: Calculate the logarithms",
                f"ln(T2/T1) = {math.log(T_ratio):.6f}",
                f"ln(p2/p1) = {math.log(p_ratio):.6f}",

                "STEP 4: Calculate each term",
                f"Cp * ln(T2/T1) = {term1:.4f}",
                f"R * ln(p2/p1) = {term2:.4f}",

                "STEP 5: Final result",
                f"Delta_s = {delta_s:.4f} J/(kg.K)"
            ]

        elif ratio_method == "2":
            rho_ratio = get_number("Enter density ratio rho2/rho1: ")

            if rho_ratio <= 0:
                print("Error: Ratios must be positive.")
                return

            Cv = get_property("Specific heat Cv", "specific_heat")
            R = get_property("Specific gas constant R", "specific_heat")

            if Cv <= 0 or R <= 0:
                print("Error: Cv and R must be positive.")
                return

            term1 = Cv * math.log(T_ratio)
            term2 = R * math.log(rho_ratio)
            delta_s = term1 + term2

            given = [
                ("Temperature ratio T2/T1", T_ratio, "dimensionless"),
                ("Density ratio rho2/rho1", rho_ratio, "dimensionless"),
                ("Specific heat Cv", Cv, "J/(kg.K)"),
                ("Specific gas constant R", R, "J/(kg.K)")
            ]

            equation_steps = [
                "STEP 1: Governing equation",
                "Delta_s = Cv * ln(T2/T1) + R * ln(rho2/rho1)",

                "STEP 2: Substitute the given ratios",
                f"Delta_s = {Cv:.4f} * ln({T_ratio:.6f})"
                f" + {R:.4f} * ln({rho_ratio:.6f})",

                "STEP 3: Calculate the logarithms",
                f"ln(T2/T1) = {math.log(T_ratio):.6f}",
                f"ln(rho2/rho1) = {math.log(rho_ratio):.6f}",

                "STEP 4: Calculate each term",
                f"Cv * ln(T2/T1) = {term1:.4f}",
                f"R * ln(rho2/rho1) = {term2:.4f}",

                "STEP 5: Final result",
                f"Delta_s = {delta_s:.4f} J/(kg.K)"
            ]

        else:
            print("Invalid ratio method.")
            return


    else:
        print("Invalid selection.")
        return

    show_solution(given, "Specific entropy change (Delta_s)", equation_steps)
    display_result("Specific entropy change", delta_s, "specific_entropy")

# ==========================================================
# 6. ISENTROPIC TEMPERATURE RELATION
# T0/T = 1 + (gamma-1)/2 * M^2
# ==========================================================

def isentropic_temperature():

    print("\n========== ISENTROPIC TEMPERATURE ==========")

    print("Equation:")
    print("T0/T = 1 + (gamma-1)/2 * M^2")

    print("\nSelect unknown:")
    print("[1] Stagnation temperature (T0)")
    print("[2] Static temperature (T)")
    print("[3] Mach number (M)")

    choice = input("Your choice: ")

    if choice not in ("1", "2", "3"):
        print("Invalid selection.")
        return

    try:

        gamma = get_gamma()
        given = []
        steps = []

        if choice == "1":

            T = get_property("Static temperature", "temperature")
            M = get_number("Mach number: ")

            if T <= 0 or M < 0:
                raise ValueError("Invalid temperature or Mach number.")

            factor = 1 + (gamma - 1) / 2 * M**2
            result = T * factor

            given = [
                ("Static temperature", T, "K"),
                ("Mach number", M, ""),
                ("Gamma", gamma, "")
            ]

            steps = [
                "Governing equation:",
                "T0/T = 1 + (gamma-1)/2 * M^2",
                "Rearrange: T0 = T * [1 + (gamma-1)/2 * M^2]",
                f"T0 = {T:.8f} * [1 + ({gamma:.8f}-1)/2 * {M:.8f}^2]",
                f"T0 = {result:.8f} K"
            ]

            show_solution(given, "Stagnation temperature (T0)", steps)
            display_result("Stagnation temperature", result, "temperature")

        elif choice == "2":

            T0 = get_property("Stagnation temperature", "temperature")
            M = get_number("Mach number: ")

            if T0 <= 0 or M < 0:
                raise ValueError("Invalid temperature or Mach number.")

            factor = 1 + (gamma - 1) / 2 * M**2
            result = T0 / factor

            given = [
                ("Stagnation temperature", T0, "K"),
                ("Mach number", M, ""),
                ("Gamma", gamma, "")
            ]

            steps = [
                "Governing equation:",
                "T0/T = 1 + (gamma-1)/2 * M^2",
                "Rearrange: T = T0 / [1 + (gamma-1)/2 * M^2]",
                f"T = {T0:.8f} / {factor:.8f}",
                f"T = {result:.8f} K"
            ]

            show_solution(given, "Static temperature (T)", steps)
            display_result("Static temperature", result, "temperature")

        else:

            T0 = get_property("Stagnation temperature", "temperature")
            T = get_property("Static temperature", "temperature")

            if T0 <= 0 or T <= 0:
                raise ValueError("Temperatures must be positive.")

            ratio = T0 / T

            if ratio < 1:
                raise ValueError("For this relation, T0/T must be >= 1.")

            result = math.sqrt(
                2 / (gamma - 1) * (ratio - 1)
            )

            given = [
                ("Stagnation temperature", T0, "K"),
                ("Static temperature", T, "K"),
                ("Gamma", gamma, "")
            ]

            steps = [
                "Governing equation:",
                "T0/T = 1 + (gamma-1)/2 * M^2",
                f"{T0:.8f}/{T:.8f} = {ratio:.8f}",
                "Rearrange:",
                "M = sqrt(2/(gamma-1) * (T0/T - 1))",
                f"M = sqrt(2/({gamma:.8f}-1) * ({ratio:.8f}-1))",
                f"M = {result:.8f}"
            ]

            show_solution(given, "Mach number (M)", steps)

            print(f"\nMach number = {result:.8f}")
            print(f"Flow classification = {classify_flow(result)}")

    except (ValueError, KeyError) as error:
        print(f"\nCalculation error: {error}")
# ==========================================================
# 6.1 ISENTROPIC RELATION 
# 
# ==========================================================


def ideal_gas_ratios_and_velocity():
    print("\n--- IDEAL GAS RATIOS AND VELOCITY ---")
    print("[1] Calculate pressure and density ratios from temperatures")
    print("[2] Calculate temperature from pressure ratio")
    print("[3] Calculate temperature from density ratio")
    print("[4] Calculate velocity using tau and Cp")
    print("[5] Calculate all ratios from temperatures")

    choice = input("Select calculation: ").strip()

    if choice not in ("1", "2", "3", "4", "5"):
        print("Invalid selection.")
        return

    if choice in ("1", "2", "3", "5"):
        gamma = get_gamma()

        if gamma <= 1:
            print("Error: gamma must be greater than 1.")
            return

        if choice in ("1", "5"):
            T1 = get_property("Initial temperature T1", "temperature")
            T2 = get_property("Final temperature T2", "temperature")

            if T1 <= 0 or T2 <= 0:
                print("Temperatures must be positive.")
                return

            tau = T2 / T1

            pressure_ratio = tau ** (gamma / (gamma - 1))
            density_ratio = tau ** (1 / (gamma - 1))

            given = [
                ("Initial temperature T1", T1, "K"),
                ("Final temperature T2", T2, "K"),
                ("Gamma", gamma, "-")
            ]

            equation_steps = [
                "STEP 1: Temperature ratio",
                "tau = T2/T1",
                f"tau = {T2:.4f}/{T1:.4f} = {tau:.6f}",

                "STEP 2: Pressure ratio",
                "p2/p1 = tau ** (gamma/(gamma-1))",
                f"p2/p1 = {tau:.6f} ** ({gamma:.4f}/({gamma:.4f}-1))",
                f"p2/p1 = {pressure_ratio:.6f}",

                "STEP 3: Density ratio",
                "rho2/rho1 = tau ** (1/(gamma-1))",
                f"rho2/rho1 = {tau:.6f} ** (1/({gamma:.4f}-1))",
                f"rho2/rho1 = {density_ratio:.6f}"
            ]

        elif choice == "2":
            pressure_ratio = get_number("Enter pressure ratio p2/p1: ")

            if pressure_ratio <= 0:
                print("Pressure ratio must be positive.")
                return

            tau = pressure_ratio ** ((gamma - 1) / gamma)

            print("\nWhich temperature do you want to find?")
            print("[1] Final temperature T2")
            print("[2] Initial temperature T1")
            target = input("Select: ").strip()

            if target == "1":
                T1 = get_property("Known initial temperature T1", "temperature")
                T2 = tau * T1
                unknown = "Final temperature T2"

            elif target == "2":
                T2 = get_property("Known final temperature T2", "temperature")
                T1 = T2 / tau
                unknown = "Initial temperature T1"

            else:
                print("Invalid selection.")
                return

            given = [
                ("Pressure ratio p2/p1", pressure_ratio, "-"),
                ("Gamma", gamma, "-"),
                ("Temperature ratio tau", tau, "-")
            ]

            equation_steps = [
                "STEP 1: Pressure-temperature relation",
                "p2/p1 = tau ** (gamma/(gamma-1))",

                "STEP 2: Rearrange to find tau",
                "tau = (p2/p1) ** ((gamma-1)/gamma)",
                f"tau = {pressure_ratio:.6f} ** (({gamma:.4f}-1)/{gamma:.4f})",
                f"tau = {tau:.6f}",

                "STEP 3: Calculate the unknown temperature",
                (
                    f"T2 = tau * T1 = {tau:.6f} * {T1:.4f} = {T2:.4f} K"
                    if target == "1"
                    else f"T1 = T2/tau = {T2:.4f}/{tau:.6f} = {T1:.4f} K"
                )
            ]

        else:
            density_ratio = get_number("Enter density ratio rho2/rho1: ")

            if density_ratio <= 0:
                print("Density ratio must be positive.")
                return

            tau = density_ratio ** (gamma - 1)

            print("\nWhich temperature do you want to find?")
            print("[1] Final temperature T2")
            print("[2] Initial temperature T1")
            target = input("Select: ").strip()

            if target == "1":
                T1 = get_property("Known initial temperature T1", "temperature")
                T2 = tau * T1
                unknown = "Final temperature T2"

            elif target == "2":
                T2 = get_property("Known final temperature T2", "temperature")
                T1 = T2 / tau
                unknown = "Initial temperature T1"

            else:
                print("Invalid selection.")
                return

            given = [
                ("Density ratio rho2/rho1", density_ratio, "-"),
                ("Gamma", gamma, "-"),
                ("Temperature ratio tau", tau, "-")
            ]

            equation_steps = [
                "STEP 1: Density-temperature relation",
                "rho2/rho1 = tau ** (1/(gamma-1))",

                "STEP 2: Rearrange to find tau",
                "tau = (rho2/rho1) ** (gamma-1)",
                f"tau = {density_ratio:.6f} ** ({gamma:.4f}-1)",
                f"tau = {tau:.6f}",

                "STEP 3: Calculate the unknown temperature",
                (
                    f"T2 = tau * T1 = {tau:.6f} * {T1:.4f} = {T2:.4f} K"
                    if target == "1"
                    else f"T1 = T2/tau = {T2:.4f}/{tau:.6f} = {T1:.4f} K"
                )
            ]

        show_solution(given, "Ideal gas property calculation", equation_steps)

        if choice in ("1", "5"):
            print("\nRESULTS")
            print(f"T2/T1       = {tau:.6f}")
            print(f"p2/p1       = {pressure_ratio:.6f}")
            print(f"rho2/rho1   = {density_ratio:.6f}")
        else:
            display_result(unknown, T2 if target == "1" else T1, "temperature")

    
    if choice == "4":
        print("\n--- VELOCITY USING TAU AND Cp ---")
        print("[1] Initial velocity is negligible (V infinity = 0)")
        print("[2] Initial velocity V infinity is given")

        velocity_choice = input("Select method: ").strip()

        if velocity_choice not in ("1", "2"):
            print("Invalid selection.")
            return

        T1 = get_property("Initial temperature T1", "temperature")
        T2 = get_property("Final temperature T2", "temperature")
        Cp = get_property("Specific heat Cp", "specific_heat")

        if T1 <= 0 or T2 <= 0 or Cp <= 0:
            print("Inputs must be positive.")
            return

        tau = T2 / T1

        if tau > 1:
            print("Error: T2 must be less than or equal to T1.")
            return

        if velocity_choice == "1":
            V_infinity = 0.0
        else:
            V_infinity = get_property(
                "Initial velocity V infinity", "velocity"
            )

        velocity_squared = (
            V_infinity**2 + 2 * Cp * T1 * (1 - tau)
        )

        velocity = math.sqrt(velocity_squared)

        given = [
            ("Initial temperature T1", T1, "K"),
            ("Final temperature T2", T2, "K"),
            ("Specific heat Cp", Cp, "J/(kg.K)"),
            ("Temperature ratio tau", tau, "-"),
            ("Initial velocity V infinity", V_infinity, "m/s")
        ]

        equation_steps = [
            "STEP 1: Calculate temperature ratio",
            f"tau = T2/T1 = {T2:.4f}/{T1:.4f} = {tau:.6f}",

            "STEP 2: Governing energy equation",
            "V2 = sqrt(V infinity^2 + 2*Cp*T1*(1-tau))",

            "STEP 3: Substitute values",
            f"V2 = sqrt({V_infinity:.4f}^2 + "
            f"2*{Cp:.4f}*{T1:.4f}*(1-{tau:.6f}))",

            "STEP 4: Calculate individual terms",
            f"V infinity^2 = {V_infinity**2:.4f}",
            f"2*Cp*T1*(1-tau) = "
            f"{2*Cp*T1*(1-tau):.4f}",

            "STEP 5: Calculate velocity squared",
            f"V2^2 = {velocity_squared:.4f}",

            "STEP 6: Final velocity",
            f"V2 = sqrt({velocity_squared:.4f})",
            f"V2 = {velocity:.4f} m/s"
        ]

        show_solution(given, "Final velocity V2", equation_steps)
        display_result("Final velocity V2", velocity, "velocity")



# ==========================================================
# 7. FLOW CLASSIFICATION
# ==========================================================

def classify_flow(M):

    if M < 0.3:
        return "Low-speed / approximately incompressible"
    elif M < 0.8:
        return "Subsonic"
    elif M < 1.2:
        return "Transonic"
    elif M < 5:
        return "Supersonic"
    else:
        return "Hypersonic"

# ==========================================================
# chapter 8 start
# ==========================================================

def normal_shock():
    while True:
        print("\n========== NORMAL SHOCK / FLOW PROPERTY CALCULATOR ==========")

        # ======================================================
        # STEP 1: GAS CONSTANTS
        # ======================================================

        gamma = get_gamma()

        r_input = input("Specific gas constant R [287 J/(kg.K)]: ").strip()
        R = 287.0 if r_input == "" else float(r_input)

        if gamma <= 1 or R <= 0:
            print("Invalid gas properties.")
            continue

        Cp = gamma * R / (gamma - 1)
        Cv = R / (gamma - 1)
        exponent = gamma / (gamma - 1)

        # ======================================================
        # STEP 2: INPUT ALL AVAILABLE DATA
        # ======================================================

        known = {}

        def ask_number(name, key):
            answer = input(f"Is {name} given? [y/N]: ").strip().lower()
            if answer == "y":
                value = float(input(f"Enter {name}: "))
                if value <= 0:
                    raise ValueError(f"{name} must be positive.")
                known[key] = value

        def ask_property(name, kind, key):
            answer = input(f"Is {name} given? [y/N]: ").strip().lower()
            if answer == "y":
                value = get_property(name, kind)
                if value <= 0:
                    raise ValueError(f"{name} must be positive.")
                known[key] = value

        print("\n--- UPSTREAM STATION (1) ---")
        print("Enter any properties supplied by the problem.")

        try:
            ask_number("Mach number M1", "M1")
            ask_property("Velocity V1", "velocity", "V1")
            ask_property("Static temperature T1", "temperature", "T1")
            ask_property("Stagnation temperature T01", "temperature", "T01")
            ask_property("Static pressure p1", "pressure", "p1")
            ask_property("Stagnation pressure p01", "pressure", "p01")
            ask_property("Static density rho1", "density", "rho1")
            ask_property("Stagnation density rho01", "density", "rho01")

            print("\n--- DOWNSTREAM STATION (2) ---")

            ask_number("Mach number M2", "M2")
            ask_property("Velocity V2", "velocity", "V2")
            ask_property("Static temperature T2", "temperature", "T2")
            ask_property("Stagnation temperature T02", "temperature", "T02")
            ask_property("Static pressure p2", "pressure", "p2")
            ask_property("Stagnation pressure p02", "pressure", "p02")
            ask_property("Static density rho2", "density", "rho2")
            ask_property("Stagnation density rho02", "density", "rho02")

        except ValueError as error:
            print(f"\nInput error: {error}")
            continue

        # ======================================================
        # STEP 3: HELPER FUNCTIONS
        # ======================================================

        def mach_from_temperature_ratio(ratio):
            if ratio < 1:
                return None

            return math.sqrt(
                2 * (ratio - 1) / (gamma - 1)
            )

        def mach_from_pressure_ratio(ratio):
            if ratio < 1:
                return None

            return math.sqrt(
                2 / (gamma - 1) *
                (ratio ** ((gamma - 1) / gamma) - 1)
            )

        def mach_from_density_ratio(ratio):
            if ratio < 1:
                return None

            return math.sqrt(
                2 / (gamma - 1) *
                (ratio ** (gamma - 1) - 1)
            )

        def mach2_from_mach1(mach):
            return math.sqrt(
                (1 + ((gamma - 1) / 2) * mach**2) /
                (gamma * mach**2 - (gamma - 1) / 2)
            )

        def mach1_from_mach2(mach):
            denominator = gamma * mach**2 - (gamma - 1) / 2

            if denominator <= 0 or mach >= 1:
                return None

            return math.sqrt(
                (1 + ((gamma - 1) / 2) * mach**2) /
                denominator
            )

        def shock_ratios(mach):
            pr = 1 + (
                2 * gamma / (gamma + 1)
            ) * (mach**2 - 1)

            rr = (
                (gamma + 1) * mach**2 /
                ((gamma - 1) * mach**2 + 2)
            )

            tr = pr / rr

            return pr, rr, tr

        def mach_from_temperature_shock_ratio(ratio):
            if ratio < 1:
                return None

            low = 1.0000001
            high = 1000.0

            for _ in range(150):
                mid = (low + high) / 2
                _, _, calculated = shock_ratios(mid)

                if calculated < ratio:
                    low = mid
                else:
                    high = mid

            return (low + high) / 2

        # ======================================================
        # STEP 4: FIND MACH NUMBER FROM UPSTREAM DATA
        # ======================================================

        M1 = known.get("M1")
        M2 = known.get("M2")

        T1 = known.get("T1")
        T01 = known.get("T01")
        p1 = known.get("p1")
        p01 = known.get("p01")
        rho1 = known.get("rho1")
        rho01 = known.get("rho01")
        V1 = known.get("V1")

        T2 = known.get("T2")
        T02 = known.get("T02")
        p2 = known.get("p2")
        p02 = known.get("p02")
        rho2 = known.get("rho2")
        rho02 = known.get("rho02")
        V2 = known.get("V2")

        # Calculate temperature from ideal gas law where possible

        if T1 is None and p1 is not None and rho1 is not None:
            T1 = p1 / (rho1 * R)

        if T2 is None and p2 is not None and rho2 is not None:
            T2 = p2 / (rho2 * R)

        # Upstream Mach from upstream stagnation/static data

        if M1 is None:
            if T1 is not None and T01 is not None:
                M1 = mach_from_temperature_ratio(T01 / T1)

            elif p1 is not None and p01 is not None:
                M1 = mach_from_pressure_ratio(p01 / p1)

            elif rho1 is not None and rho01 is not None:
                M1 = mach_from_density_ratio(rho01 / rho1)

            elif V1 is not None and T1 is not None:
                M1 = V1 / math.sqrt(gamma * R * T1)

            elif V1 is not None and T01 is not None:
                denominator = gamma * R * T01 - (
                    (gamma - 1) / 2
                ) * V1**2

                if denominator > 0:
                    M1 = V1 / math.sqrt(denominator)

        # Downstream Mach from downstream stagnation/static data

        if M2 is None:
            if T2 is not None and T02 is not None:
                M2 = mach_from_temperature_ratio(T02 / T2)

            elif p2 is not None and p02 is not None:
                M2 = mach_from_pressure_ratio(p02 / p2)

            elif rho2 is not None and rho02 is not None:
                M2 = mach_from_density_ratio(rho02 / rho2)

            elif V2 is not None and T2 is not None:
                M2 = V2 / math.sqrt(gamma * R * T2)

        # Recover upstream Mach from downstream Mach

        if M1 is None and M2 is not None:
            M1 = mach1_from_mach2(M2)

        # ======================================================
        # STEP 5: FIND MACH FROM CROSS-STATION RATIOS
        # ======================================================

        if M1 is None:

            # Pressure ratio p2/p1

            if p1 is not None and p2 is not None:
                ratio = p2 / p1

                if ratio >= 1:
                    M1 = math.sqrt(
                        1 + ((gamma + 1) / (2 * gamma)) *
                        (ratio - 1)
                    )

            # Density ratio rho2/rho1

            if M1 is None and rho1 is not None and rho2 is not None:
                ratio = rho2 / rho1

                denominator = (gamma + 1) - ratio * (gamma - 1)

                if 1 <= ratio < (gamma + 1) / (gamma - 1):
                    M1 = math.sqrt(
                        2 * ratio / denominator
                    )

            # Temperature ratio T2/T1

            if M1 is None and T1 is not None and T2 is not None:
                M1 = mach_from_temperature_shock_ratio(T2 / T1)

        # ======================================================
        # STEP 6: CHECK WHETHER MACH NUMBER IS DETERMINED
        # ======================================================

        if M1 is None:
            print("\nInsufficient information to determine the flow Mach number.")
            print("\nExamples of sufficient input combinations:")
            print("  V1 and T1")
            print("  V1 and T01")
            print("  p1 and p01")
            print("  T1 and T01")
            print("  p2 and p1")
            print("  M2 and a downstream static property")
            print("  V2 and T2")
            print("  M1 directly")
            continue

        if M1 <= 0:
            print("Invalid upstream Mach number.")
            continue

        # ======================================================
        # STEP 7: DETERMINE SHOCK RELATIONS
        # ======================================================

        shock_exists = M1 > 1

        if shock_exists:
            M2_calculated = mach2_from_mach1(M1)

            pressure_ratio, density_ratio, temperature_ratio = shock_ratios(M1)

            # Use calculated downstream Mach if not supplied
            if M2 is None:
                M2 = M2_calculated

        else:
            M2_calculated = None
            pressure_ratio = None
            density_ratio = None
            temperature_ratio = None

        # ======================================================
        # STEP 8: CALCULATE MISSING STATIC PROPERTIES
        # ======================================================

        if shock_exists:

            # Temperature propagation
            if T1 is None and T2 is not None:
                T1 = T2 / temperature_ratio

            if T2 is None and T1 is not None:
                T2 = T1 * temperature_ratio

            # Pressure propagation
            if p1 is None and p2 is not None:
                p1 = p2 / pressure_ratio

            if p2 is None and p1 is not None:
                p2 = p1 * pressure_ratio

            # Density propagation
            if rho1 is None and rho2 is not None:
                rho1 = rho2 / density_ratio

            if rho2 is None and rho1 is not None:
                rho2 = rho1 * density_ratio

        # Ideal gas law at both stations

        if T1 is None and p1 is not None and rho1 is not None:
            T1 = p1 / (rho1 * R)

        if T2 is None and p2 is not None and rho2 is not None:
            T2 = p2 / (rho2 * R)

        if rho1 is None and p1 is not None and T1 is not None:
            rho1 = p1 / (R * T1)

        if rho2 is None and p2 is not None and T2 is not None:
            rho2 = p2 / (R * T2)

        if p1 is None and rho1 is not None and T1 is not None:
            p1 = rho1 * R * T1

        if p2 is None and rho2 is not None and T2 is not None:
            p2 = rho2 * R * T2

        # ======================================================
        # STEP 9: STAGNATION PROPERTIES
        # ======================================================

        if T1 is not None:
            T01_calculated = T1 * (
                1 + ((gamma - 1) / 2) * M1**2
            )
            if T01 is None:
                T01 = T01_calculated

        if T2 is not None and M2 is not None:
            T02_calculated = T2 * (
                1 + ((gamma - 1) / 2) * M2**2
            )
            if T02 is None:
                T02 = T02_calculated

        if shock_exists and T01 is not None:
            T02 = T01

        if p1 is not None:
            p01_calculated = p1 * (
                1 + ((gamma - 1) / 2) * M1**2
            )**exponent

            if p01 is None:
                p01 = p01_calculated

        if p2 is not None and M2 is not None:
            p02_calculated = p2 * (
                1 + ((gamma - 1) / 2) * M2**2
            )**exponent

            if p02 is None:
                p02 = p02_calculated

        if rho1 is not None:
            rho01_calculated = rho1 * (
                1 + ((gamma - 1) / 2) * M1**2
            )**(1 / (gamma - 1))

            if rho01 is None:
                rho01 = rho01_calculated

        if rho2 is not None and M2 is not None:
            rho02_calculated = rho2 * (
                1 + ((gamma - 1) / 2) * M2**2
            )**(1 / (gamma - 1))

            if rho02 is None:
                rho02 = rho02_calculated

        # ======================================================
        # STEP 10: VELOCITY AND SPEED OF SOUND
        # ======================================================

        a1 = math.sqrt(gamma * R * T1) if T1 is not None else None
        a2 = math.sqrt(gamma * R * T2) if T2 is not None else None

        if V1 is None and a1 is not None:
            V1 = M1 * a1

        if V2 is None and a2 is not None and M2 is not None:
            V2 = M2 * a2

        # ======================================================
        # STEP 11: CRITICAL / STAR PROPERTIES
        # ======================================================

        critical_factor = 2 / (gamma + 1)

        M1_star = M1 * math.sqrt(
            (gamma + 1) /
            (2 + (gamma - 1) * M1**2)
        )

        a1_star = (
            math.sqrt(2 * gamma * R * T01 / (gamma + 1))
            if T01 is not None else None
        )

        T1_star = (
            T01 * critical_factor
            if T01 is not None else None
        )

        p1_star = (
            p01 * critical_factor**exponent
            if p01 is not None else None
        )

        rho1_star = (
            rho01 * critical_factor**(1 / (gamma - 1))
            if rho01 is not None else None
        )

        V1_star = a1_star

        if shock_exists and M2 is not None:

            M2_star = M2 * math.sqrt(
                (gamma + 1) /
                (2 + (gamma - 1) * M2**2)
            )

            a2_star = (
                math.sqrt(2 * gamma * R * T02 / (gamma + 1))
                if T02 is not None else None
            )

            T2_star = (
                T02 * critical_factor
                if T02 is not None else None
            )

            p2_star = (
                p02 * critical_factor**exponent
                if p02 is not None else None
            )

            rho2_star = (
                rho02 * critical_factor**(1 / (gamma - 1))
                if rho02 is not None else None
            )

            V2_star = a2_star

        else:
            M2_star = None
            a2_star = None
            T2_star = None
            p2_star = None
            rho2_star = None
            V2_star = None

        # ======================================================
        # STEP 12: FINAL RESULTS TABLE
        # ======================================================

        def fmt(value, unit=""):
            if value is None:
                return "N/A"
            return f"{value:.5f} {unit}".strip()

        print("\n========== COMPLETE FLOW PROPERTY TABLE ==========")
        print(f"{'PROPERTY':<26}{'UPSTREAM (1)':>20}{'DOWNSTREAM (2)':>20}")
        print("-" * 66)

        rows = [
            ("Mach number M", M1, M2, ""),
            ("Star Mach number M*", M1_star, M2_star, ""),
            ("Velocity V", V1, V2, "m/s"),
            ("Speed of sound a", a1, a2, "m/s"),
            ("Critical speed a*", a1_star, a2_star, "m/s"),
            ("Static temperature T", T1, T2, "K"),
            ("Stagnation temperature T0", T01, T02, "K"),
            ("Critical temperature T*", T1_star, T2_star, "K"),
            ("Static pressure p", p1, p2, "Pa"),
            ("Stagnation pressure p0", p01, p02, "Pa"),
            ("Critical pressure p*", p1_star, p2_star, "Pa"),
            ("Static density rho", rho1, rho2, "kg/m^3"),
            ("Stagnation density rho0", rho01, rho02, "kg/m^3"),
            ("Critical density rho*", rho1_star, rho2_star, "kg/m^3"),
            ("Critical velocity V*", V1_star, V2_star, "m/s"),
        ]

        for name, value1, value2, unit in rows:
            print(
                f"{name:<26}"
                f"{fmt(value1, unit):>20}"
                f"{fmt(value2, unit):>20}"
            )

        # ======================================================
        # STEP 13: RATIOS
        # ======================================================

        print("\n========== NORMAL SHOCK RATIOS ==========")

        if shock_exists:
            print(f"M2/M1       = {fmt(M2 / M1)}")
            print(f"p2/p1       = {fmt(pressure_ratio)}")
            print(f"rho2/rho1   = {fmt(density_ratio)}")
            print(f"T2/T1       = {fmt(temperature_ratio)}")

            if p01 is not None and p02 is not None:
                print(f"p02/p01     = {fmt(p02 / p01)}")

            print("T02/T01     = 1.00000 (adiabatic normal shock)")

        else:
            print("No normal shock: M1 is not greater than 1.")
            print("General flow and critical properties are still calculated.")

        # ======================================================
        # STEP 14: STEP-BY-STEP SOLUTION
        # ======================================================

        given = [
            ("Specific heat ratio gamma", gamma, ""),
            ("Specific gas constant R", R, "J/(kg.K)"),
            ("Cp", Cp, "J/(kg.K)"),
            ("Cv", Cv, "J/(kg.K)"),
            ("Upstream Mach number M1", M1, ""),
        ]

        for key, label, unit in [
            ("V1", "Given upstream velocity", "m/s"),
            ("T1", "Given upstream static temperature", "K"),
            ("T01", "Given upstream stagnation temperature", "K"),
            ("p1", "Given upstream static pressure", "Pa"),
            ("p01", "Given upstream stagnation pressure", "Pa"),
            ("rho1", "Given upstream static density", "kg/m^3"),
            ("rho01", "Given upstream stagnation density", "kg/m^3"),
            ("M2", "Given downstream Mach number", ""),
            ("V2", "Given downstream velocity", "m/s"),
            ("T2", "Given downstream static temperature", "K"),
            ("T02", "Given downstream stagnation temperature", "K"),
            ("p2", "Given downstream static pressure", "Pa"),
            ("p02", "Given downstream stagnation pressure", "Pa"),
            ("rho2", "Given downstream static density", "kg/m^3"),
            ("rho02", "Given downstream stagnation density", "kg/m^3"),
        ]:
            if key in known:
                given.append((label, known[key], unit))

        equation_steps = [
            "1. Determine Mach number from the available upstream/downstream data.",
            f"M1 = {M1:.6f}",
        ]

        if shock_exists:
            equation_steps.extend([
                "\n2. Normal shock Mach relation:",
                "M2 = sqrt([1+(gamma-1)*M1^2/2] / "
                "[gamma*M1^2-(gamma-1)/2])",
                f"M2 = {M2:.6f}",

                "\n3. Normal shock pressure ratio:",
                "p2/p1 = 1 + [2*gamma/(gamma+1)]*(M1^2-1)",
                f"p2/p1 = {pressure_ratio:.6f}",

                "\n4. Normal shock density ratio:",
                "rho2/rho1 = [(gamma+1)*M1^2] / "
                "[(gamma-1)*M1^2+2]",
                f"rho2/rho1 = {density_ratio:.6f}",

                "\n5. Normal shock temperature ratio:",
                "T2/T1 = (p2/p1)/(rho2/rho1)",
                f"T2/T1 = {temperature_ratio:.6f}",

                "\n6. Critical Mach number:",
                "M* = M*sqrt((gamma+1)/(2+(gamma-1)*M^2))",
                f"Upstream M1* = {M1_star:.6f}",
                f"Downstream M2* = {M2_star:.6f}",

                "\n7. Critical speed of sound:",
                "a* = sqrt(2*gamma*R*T0/(gamma+1))",
                f"Upstream a1* = {fmt(a1_star, 'm/s')}",
                f"Downstream a2* = {fmt(a2_star, 'm/s')}",
            ])

        else:
            equation_steps.append(
                "Normal shock equations were not applied because M1 <= 1."
            )

        show_solution(
            given,
            "Normal shock and compressible flow properties",
            equation_steps
        )

        # ======================================================
        # STEP 15: REPEAT OR RETURN
        # ======================================================

        print("\n[1] Calculate another case")
        print("[0] Return to Chapter 8 menu")

        again = input("Select: ").strip()

        if again != "1":
            break

def rayleigh_pitot():
    while True:
        print("\n========== RAYLEIGH PITOT-TUBE CALCULATOR ==========")
        print("Anderson - Fundamentals of Aerodynamics")
        print("Chapter 8, Equation 8.80")

        # ======================================================
        # STEP 1: GAS CONSTANTS
        # ======================================================

        gamma = get_gamma()

        r_input = input(
            "Specific gas constant R [287 J/(kg.K)]: "
        ).strip()

        R = 287.0 if r_input == "" else float(r_input)

        if gamma <= 1 or R <= 0:
            print("Invalid gas properties.")
            continue

        exponent = gamma / (gamma - 1)
        Cp = gamma * R / (gamma - 1)

        # ======================================================
        # STEP 2: INPUT DATA
        # ======================================================

        print("\n--- AVAILABLE INPUT DATA ---")

        print("[1] Enter Pitot pressure p02 and static pressure p1")
        print("[2] Enter pressure ratio p02/p1 directly")
        print("[3] Enter Mach number M1 directly")

        choice = input("Select input method: ").strip()

        p02 = None
        p1 = None
        pressure_ratio = None
        M1 = None

        try:

            if choice == "1":
                p02 = get_property(
                    "Pitot pressure p02", "pressure"
                )

                p1 = get_property(
                    "Freestream static pressure p1", "pressure"
                )

                if p02 <= 0 or p1 <= 0:
                    raise ValueError("Pressures must be positive.")

                pressure_ratio = p02 / p1

            elif choice == "2":
                pressure_ratio = float(
                    input("Enter pressure ratio p02/p1: ")
                )

                if pressure_ratio <= 0:
                    raise ValueError("Pressure ratio must be positive.")

            elif choice == "3":
                M1 = float(input("Enter freestream Mach number M1: "))

                if M1 <= 0:
                    raise ValueError("Mach number must be positive.")

            else:
                print("Invalid selection.")
                continue

            # Optional temperature for velocity calculation

            T1 = None

            answer = input(
                "\nIs freestream static temperature T1 given? [y/N]: "
            ).strip().lower()

            if answer == "y":
                T1 = get_property(
                    "Freestream static temperature T1", "temperature"
                )

                if T1 <= 0:
                    raise ValueError("Temperature must be positive.")

        except ValueError as error:
            print(f"\nInput error: {error}")
            continue

        # ======================================================
        # STEP 3: EQUATION FUNCTIONS
        # ======================================================

        def isentropic_pitot_ratio(mach):
            return (
                1 + ((gamma - 1) / 2) * mach**2
            )**exponent

        def rayleigh_pitot_ratio(mach):
            first_term = (
                ((gamma + 1)**2 * mach**2) /
                (4 * gamma * mach**2 - 2 * (gamma - 1))
            )**exponent

            second_term = (
                (1 - gamma + 2 * gamma * mach**2) /
                (gamma + 1)
            )

            return first_term * second_term

        # ======================================================
        # STEP 4: DETERMINE FLOW REGIME
        # ======================================================

        critical_ratio = isentropic_pitot_ratio(1.0)

        if M1 is not None:

            if M1 < 1:
                regime = "SUBSONIC"
                pressure_ratio = isentropic_pitot_ratio(M1)

            elif M1 > 1:
                regime = "SUPERSONIC"
                pressure_ratio = rayleigh_pitot_ratio(M1)

            else:
                regime = "SONIC"
                pressure_ratio = critical_ratio

        else:

            if pressure_ratio < 1:
                print("\nInvalid Pitot pressure ratio.")
                print("The ratio must be at least 1.")
                continue

            if pressure_ratio < critical_ratio:

                regime = "SUBSONIC"

                # Invert isentropic Pitot equation

                M1 = math.sqrt(
                    2 / (gamma - 1) *
                    (
                        pressure_ratio**(
                            (gamma - 1) / gamma
                        ) - 1
                    )
                )

            elif math.isclose(
                pressure_ratio,
                critical_ratio,
                rel_tol=1e-8
            ):

                regime = "SONIC"
                M1 = 1.0

            else:

                regime = "SUPERSONIC"

                # Invert Rayleigh Pitot equation using bisection

                low = 1.0
                high = 100.0

                if rayleigh_pitot_ratio(high) < pressure_ratio:
                    print("\nPressure ratio is outside the solver range.")
                    continue

                for _ in range(200):

                    mid = (low + high) / 2

                    calculated_ratio = rayleigh_pitot_ratio(mid)

                    if calculated_ratio < pressure_ratio:
                        low = mid
                    else:
                        high = mid

                M1 = (low + high) / 2

        # ======================================================
        # STEP 5: CALCULATE FINAL PRESSURE RATIO
        # ======================================================

        if M1 < 1:

            calculated_ratio = isentropic_pitot_ratio(M1)
            equation_used = "Isentropic Pitot relation"

        elif M1 > 1:

            calculated_ratio = rayleigh_pitot_ratio(M1)
            equation_used = "Rayleigh Pitot equation (8.80)"

        else:

            calculated_ratio = critical_ratio
            equation_used = "Sonic condition"

        # ======================================================
        # STEP 6: FREESTREAM PROPERTIES
        # ======================================================

        a1 = None
        V1 = None

        if T1 is not None:

            a1 = math.sqrt(gamma * R * T1)
            V1 = M1 * a1

        # Recover p02 if p1 is known

        if p02 is None and p1 is not None:
            p02 = calculated_ratio * p1

        # Recover p1 if p02 is known

        if p1 is None and p02 is not None:
            p1 = p02 / calculated_ratio

        # ======================================================
        # STEP 7: DISPLAY RESULTS
        # ======================================================

        print("\n========== RAYLEIGH PITOT RESULTS ==========")

        print(f"Flow regime             : {regime}")
        print(f"Specific heat ratio     : {gamma:.6f}")
        print(f"Specific gas constant   : {R:.4f} J/(kg.K)")
        print(f"Mach number M1          : {M1:.6f}")
        print(f"Pressure ratio p02/p1   : {calculated_ratio:.6f}")
        print(f"Critical ratio at M=1   : {critical_ratio:.6f}")
        print(f"Equation used           : {equation_used}")

        if p02 is not None:
            print(f"Pitot pressure p02      : {p02:.5f} Pa")

        if p1 is not None:
            print(f"Static pressure p1      : {p1:.5f} Pa")

        if T1 is not None:
            print(f"Static temperature T1   : {T1:.5f} K")
            print(f"Speed of sound a1       : {a1:.5f} m/s")
            print(f"Freestream velocity V1  : {V1:.5f} m/s")

        # ======================================================
        # STEP 8: STEP-BY-STEP SOLUTION
        # ======================================================

        given = [
            ("Specific heat ratio gamma", gamma, ""),
            ("Specific gas constant R", R, "J/(kg.K)")
        ]

        if p02 is not None:
            given.append(("Pitot pressure p02", p02, "Pa"))

        if p1 is not None:
            given.append(("Static pressure p1", p1, "Pa"))

        if T1 is not None:
            given.append(("Static temperature T1", T1, "K"))

        if choice == "2":
            given.append(
                ("Given pressure ratio p02/p1", pressure_ratio, "")
            )

        if choice == "3":
            given.append(("Given Mach number M1", M1, ""))

        equation_steps = [
            "1. Calculate the critical pressure ratio at M1 = 1:",
            "p02/p1 = [1 + (gamma-1)/2]^[gamma/(gamma-1)]",
            f"Critical ratio = {critical_ratio:.6f}",

            "\n2. Determine the flow regime:",
            f"Regime = {regime}",

            "\n3. Selected equation:",
            equation_used
        ]

        if M1 < 1:

            equation_steps.extend([
                "\n4. Subsonic isentropic Pitot relation:",
                "p02/p1 = [1+(gamma-1)*M1^2/2]^[gamma/(gamma-1)]",

                "\nRearrange:",
                "M1 = sqrt(2/(gamma-1) * "
                "[(p02/p1)^((gamma-1)/gamma)-1])",

                f"\np02/p1 = {calculated_ratio:.6f}",
                f"M1 = {M1:.6f}"
            ])

        elif M1 > 1:

            first_term = (
                ((gamma + 1)**2 * M1**2) /
                (4 * gamma * M1**2 - 2 * (gamma - 1))
            )

            second_term = (
                (1 - gamma + 2 * gamma * M1**2) /
                (gamma + 1)
            )

            equation_steps.extend([
                "\n4. Anderson Rayleigh Pitot equation (8.80):",

                "p02/p1 = [((gamma+1)^2*M1^2)/"
                "(4*gamma*M1^2-2*(gamma-1))]"
                "^[gamma/(gamma-1)]",

                "* [(1-gamma+2*gamma*M1^2)/(gamma+1)]",

                "\n5. First bracket:",

                f"First bracket = {first_term:.8f}",
                f"First bracket raised to exponent = "
                f"{first_term**exponent:.8f}",

                "\n6. Second bracket:",

                f"Second bracket = {second_term:.8f}",

                "\n7. Multiply both terms:",

                f"p02/p1 = {calculated_ratio:.8f}",

                "\n8. Determine M1:",
                "Numerical solution using bisection method.",
                f"Final M1 = {M1:.8f}"
            ])

        else:

            equation_steps.extend([
                "\n4. Sonic condition:",
                "M1 = 1",
                f"p02/p1 = {critical_ratio:.8f}"
            ])

        if T1 is not None:

            equation_steps.extend([
                "\n9. Speed of sound:",
                "a1 = sqrt(gamma*R*T1)",
                f"a1 = {a1:.6f} m/s",

                "\n10. Freestream velocity:",
                "V1 = M1*a1",
                f"V1 = {V1:.6f} m/s"
            ])

        show_solution(
            given,
            "Rayleigh Pitot Tube - Anderson Equation 8.80",
            equation_steps
        )

        # ======================================================
        # STEP 9: REPEAT
        # ======================================================

        print("\n[1] Calculate another case")
        print("[0] Return to Chapter 8 menu")

        again = input("Select: ").strip()

        if again != "1":
            break

# ==========================================================
# 8. CHAPTER 7 MENU
# ==========================================================


def chapter_7():

    while True:

        print("\n========================================")
        print("CHAPTER 7 - CALCULATION MENU")
        print("========================================")

        print("\n[1] Ideal gas equation")
        print("[2] Mach number")
        print("[3] Isentropic temperature relation")

        print("\n--- THERMODYNAMICS ---")
        print("[4] Cp, Cv, R and gamma")
        print("[5] Enthalpy and internal energy")
        print("[6] Entropy")
        print("[7] Ideal gas ratios and velocity")

        print("\n[0] Return to main menu")

        choice = input("\nSelect equation: ")

        if choice == "1":
            ideal_gas()

        elif choice == "2":
            mach_calculator()

        elif choice == "3":
            isentropic_temperature()

        elif choice == "4":
            thermodynamic_properties()

        elif choice == "5":
            energy_properties()
        elif choice == "6":
            entropy_change()
        elif choice == "7":
            ideal_gas_ratios_and_velocity()


        elif choice == "0":
            break

        else:
            print("Invalid selection.")

# ==========================================================
# 9. Chapter 8 Menu
# ==========================================================

def chapter_8():
    while True:
        print("\n========== CHAPTER 8 ==========")
        print("[1] Normal shock calculator")
        print("[2] Rayleigh Pitot-tube calculator")
        print("[0] Return")

        choice = input("Select an option: ").strip()

        if choice == "1":
            normal_shock()
        elif choice == "2":
            rayleigh_pitot()

        elif choice == "0":
            break

        else:
            print("Invalid selection.")


# ==========================================================
# CHAPTER 9 - OBLIQUE SHOCKS, EXPANSIONS AND SHOCK SEQUENCES
# ANDERSON AERODYNAMICS
# ==========================================================

def chapter9():

    # ==========================================================
    # CHAPTER 9 - SEQUENTIAL COMPRESSIBLE FLOW SOLVER
    # ==========================================================

    # ----------------------------------------------------------
    # INPUT HELPERS
    # ----------------------------------------------------------

    def ask_float(prompt, default=None, minimum=None):
        while True:
            raw = input(prompt).strip()

            if raw == "" and default is not None:
                return default

            try:
                value = float(raw)

                if minimum is not None and value <= minimum:
                    print(f"Enter a value greater than {minimum}.")
                    continue

                return value

            except ValueError:
                print("Invalid input. Enter a numerical value.")

    def ask_optional(prompt, minimum=None):
        while True:
            raw = input(prompt).strip()

            if raw == "":
                return None

            try:
                value = float(raw)

                if minimum is not None and value <= minimum:
                    print(f"Enter a value greater than {minimum}, or press Enter.")
                    continue

                return value

            except ValueError:
                print("Invalid input. Enter a number or press Enter.")

    def ask_choice(prompt, choices):
        while True:
            answer = input(prompt).strip().lower()

            if answer in choices:
                return answer

            print("Choose:", ", ".join(choices))

    def ask_yes_no(prompt):
        while True:
            answer = input(prompt + " (y/n): ").strip().lower()

            if answer in ("y", "yes"):
                return True

            if answer in ("n", "no"):
                return False

            print("Enter y or n.")

    def rad(value):
        return math.radians(value)

    def deg(value):
        return math.degrees(value)

    # ----------------------------------------------------------
    # FLOW EQUATIONS
    # ----------------------------------------------------------

    def theta_from_beta(M, beta, gamma):
        numerator = (
            2.0 * (M**2 * math.sin(beta)**2 - 1.0)
            / math.tan(beta)
        )

        denominator = (
            M**2 * (gamma + math.cos(2.0 * beta)) + 2.0
        )

        return math.atan(numerator / denominator)

    def mach_angle(M):
        if M < 1.0:
            return None
        return math.asin(1.0 / M)

    def normal_mach_downstream(Mn1, gamma):
        numerator = 1.0 + (gamma - 1.0) * Mn1**2 / 2.0
        denominator = gamma * Mn1**2 - (gamma - 1.0) / 2.0

        return math.sqrt(numerator / denominator)

    def shock_ratios(Mn1, gamma):
        p_ratio = (
            1.0 + 2.0 * gamma / (gamma + 1.0)
            * (Mn1**2 - 1.0)
        )

        rho_ratio = (
            (gamma + 1.0) * Mn1**2
            / ((gamma - 1.0) * Mn1**2 + 2.0)
        )

        T_ratio = p_ratio / rho_ratio

        return p_ratio, rho_ratio, T_ratio

    # ----------------------------------------------------------
    # NUMERICAL ROOT FINDER
    # ----------------------------------------------------------

    def bisect(function, target, low, high, iterations=100):
        f_low = function(low) - target
        f_high = function(high) - target

        if abs(f_low) < 1e-12:
            return low

        if abs(f_high) < 1e-12:
            return high

        if f_low * f_high > 0:
            return None

        for _ in range(iterations):
            middle = (low + high) / 2.0
            f_middle = function(middle) - target

            if abs(f_middle) < 1e-12:
                return middle

            if f_low * f_middle <= 0:
                high = middle
                f_high = f_middle
            else:
                low = middle
                f_low = f_middle

        return (low + high) / 2.0

    def find_roots(function, target, low, high, samples=6000):
        roots = []

        previous_x = low
        previous_f = function(previous_x) - target

        for i in range(1, samples + 1):
            current_x = low + (high - low) * i / samples
            current_f = function(current_x) - target

            if previous_f * current_f < 0:
                root = bisect(
                    function, target, previous_x, current_x
                )

                if root is not None:
                    if not roots or abs(root - roots[-1]) > 1e-6:
                        roots.append(root)

            previous_x = current_x
            previous_f = current_f

        return roots

    # ----------------------------------------------------------
    # FIND WEAK AND STRONG BETA FROM THETA
    # ----------------------------------------------------------

    def find_shock_roots(M, theta, gamma):
        mu = mach_angle(M)

        if mu is None:
            return []

        beta_min = mu + 1e-8
        beta_max = math.pi / 2.0 - 1e-8

        maximum_theta = max(
            theta_from_beta(
                M,
                beta_min + (beta_max - beta_min) * i / 10000,
                gamma
            )
            for i in range(1, 10000)
        )

        if theta > maximum_theta + 1e-8:
            return []

        return find_roots(
            lambda beta: theta_from_beta(M, beta, gamma),
            theta,
            beta_min,
            beta_max
        )

    # ----------------------------------------------------------
    # PRANDTL-MEYER FUNCTION
    # ----------------------------------------------------------

    def prandtl_meyer(M, gamma):
        if M < 1.0:
            raise ValueError("Prandtl-Meyer function requires M >= 1.")

        first = math.sqrt((gamma + 1.0) / (gamma - 1.0))

        second = math.sqrt(
            (gamma - 1.0) / (gamma + 1.0) * (M**2 - 1.0)
        )

        return (
            first * math.atan(second)
            - math.atan(math.sqrt(M**2 - 1.0))
        )

    def inverse_prandtl_meyer(target, gamma):
        maximum = (
            math.pi / 2.0
            * (math.sqrt((gamma + 1.0) / (gamma - 1.0)) - 1.0)
        )

        if target < 0 or target >= maximum:
            return None

        low = 1.0
        high = 2.0

        while prandtl_meyer(high, gamma) < target:
            high *= 2.0

            if high > 1e7:
                return None

        for _ in range(120):
            middle = (low + high) / 2.0

            if prandtl_meyer(middle, gamma) < target:
                low = middle
            else:
                high = middle

        return (low + high) / 2.0

    # ----------------------------------------------------------
    # STATE PROPERTY HANDLING
    # ----------------------------------------------------------

    property_names = {
        "M": "Mach number M",
        "p": "Static pressure p [Pa]",
        "T": "Static temperature T [K]",
        "rho": "Static density rho [kg/m3]",
        "p0": "Stagnation pressure p0 [Pa]",
        "T0": "Stagnation temperature T0 [K]",
        "rho0": "Stagnation density rho0 [kg/m3]",
        "V": "Velocity V [m/s]",
        "a": "Speed of sound a [m/s]"
    }

    def complete_state(state):
        s = state.copy()

        M = s.get("M")

        if M is not None:
            factor_T = 1.0 + (gamma - 1.0) * M**2 / 2.0

            factor_p = factor_T ** (
                gamma / (gamma - 1.0)
            )

            factor_rho = factor_T ** (
                1.0 / (gamma - 1.0)
            )

            if s.get("T") is not None and s.get("T0") is None:
                s["T0"] = s["T"] * factor_T

            elif s.get("T0") is not None and s.get("T") is None:
                s["T"] = s["T0"] / factor_T

            if s.get("p") is not None and s.get("p0") is None:
                s["p0"] = s["p"] * factor_p

            elif s.get("p0") is not None and s.get("p") is None:
                s["p"] = s["p0"] / factor_p

            if s.get("rho") is not None and s.get("rho0") is None:
                s["rho0"] = s["rho"] * factor_rho

            elif s.get("rho0") is not None and s.get("rho") is None:
                s["rho"] = s["rho0"] / factor_rho

        # Ideal gas law
        p = s.get("p")
        T = s.get("T")
        rho = s.get("rho")

        if p is not None and T is not None and rho is None:
            s["rho"] = p / (R * T)

        elif p is not None and rho is not None and T is None:
            s["T"] = p / (rho * R)

        elif T is not None and rho is not None and p is None:
            s["p"] = rho * R * T

        # Speed of sound
        if s.get("T") is not None and s.get("a") is None:
            s["a"] = math.sqrt(gamma * R * s["T"])

        # Mach and velocity
        if s.get("M") is not None and s.get("a") is not None:
            if s.get("V") is None:
                s["V"] = s["M"] * s["a"]

        elif s.get("V") is not None and s.get("a") is not None:
            if s["a"] > 0:
                s["M"] = s["V"] / s["a"]

        return s

    def collect_region_properties(region_number, state):
        print(
            f"\n========== REGION {region_number} KNOWN PROPERTIES =========="
        )

        if not ask_yes_no("Do you have additional known properties for this region?"):
            return complete_state(state)

        print("Enter known values in SI units.")
        print("Press Enter for any property that is not given.")

        supplied = {}

        for key, description in property_names.items():
            supplied[key] = ask_optional(
                description + ": ",
                minimum=0.0
            )

        print("\n--- Comparison with calculated values ---")

        for key, value in supplied.items():
            if value is None:
                continue

            calculated = state.get(key)

            if calculated is not None:
                difference = value - calculated
                percentage = (
                    abs(difference) / max(abs(calculated), 1e-12) * 100.0
                )

                print(
                    f"{key}: calculated = {calculated:.6g}, "
                    f"supplied = {value:.6g}, "
                    f"difference = {difference:.6g} "
                    f"({percentage:.3f}%)"
                )
            else:
                print(
                    f"{key}: supplied = {value:.6g}; "
                    "no calculated value to compare."
                )

            # Supplied values become the working values.
            state[key] = value

        return complete_state(state)

    # ----------------------------------------------------------
    # INITIAL REGION INPUT
    # ----------------------------------------------------------

    def initial_region():
        print("\n========== REGION 1: FREESTREAM ==========")
        print("Select the type of initial flow data:")
        print("[1] Mach number M (DEFAULT)")
        print("[2] Velocity V and speed of sound a")
        print("[3] Velocity V and static temperature T")

        data_type = input("Select data type [1]: ").strip()

        if data_type == "":
            data_type = "1"

        state = {
            "M": None,
            "p": None,
            "T": None,
            "rho": None,
            "p0": None,
            "T0": None,
            "rho0": None,
            "V": None,
            "a": None
        }

        if data_type == "1":
            state["M"] = ask_float(
                "Freestream Mach number M1: ",
                minimum=0.0
            )

        elif data_type == "2":
            state["V"] = ask_float(
                "Freestream velocity V1 [m/s]: ",
                minimum=0.0
            )

            state["a"] = ask_float(
                "Speed of sound a1 [m/s]: ",
                minimum=0.0
            )

            state["M"] = state["V"] / state["a"]

        elif data_type == "3":
            state["V"] = ask_float(
                "Freestream velocity V1 [m/s]: ",
                minimum=0.0
            )

            state["T"] = ask_float(
                "Static temperature T1 [K]: ",
                minimum=0.0
            )

            state["a"] = math.sqrt(gamma * R * state["T"])
            state["M"] = state["V"] / state["a"]

        else:
            print("Invalid data type.")
            return None

        print(f"\nCalculated freestream Mach number = {state['M']:.8f}")

        return collect_region_properties(1, state)

    # ----------------------------------------------------------
    # OBLIQUE SHOCK
    # ----------------------------------------------------------

    def apply_oblique_shock(state, layer_number):
        M1 = state.get("M")

        if M1 is None or M1 <= 1.0:
            print("An oblique shock requires M1 > 1.")
            return None, None

        print(f"\n========== LAYER {layer_number}: OBLIQUE SHOCK ==========")
        print("[1] Turning angle theta is given")
        print("[2] Shock angle beta is given")
        print("[3] Downstream Mach number M2 is given")
        print("[4] Pressure ratio p2/p1 is given")
        print("[5] Both theta and beta are given")

        mode = ask_choice("Selection: ", ["1", "2", "3", "4", "5"])

        theta_given = None
        beta_given = None
        M2_given = None
        p_ratio_given = None

        if mode in ("1", "5"):
            theta_given = rad(
                ask_float("Turning angle theta [degrees]: ", minimum=0.0)
            )

        if mode in ("2", "5"):
            beta_given = rad(
                ask_float("Shock angle beta [degrees]: ", minimum=0.0)
            )

        if mode == "3":
            M2_given = ask_float("Downstream Mach number M2: ", minimum=0.0)

        if mode == "4":
            p_ratio_given = ask_float("Pressure ratio p2/p1: ", minimum=0.0)

        mu1 = mach_angle(M1)

        # Determine beta and theta.
        if beta_given is not None:
            beta = beta_given

            if beta <= mu1 or beta >= math.pi / 2:
                print(
                    f"Invalid beta. It must be between "
                    f"{deg(mu1):.5f} and 90 degrees."
                )
                return None, None

            theta = theta_from_beta(M1, beta, gamma)

            if theta <= 0:
                print("Invalid compressive shock angle.")
                return None, None

            if theta_given is not None:
                print(
                    f"\nGiven theta = {deg(theta_given):.6f} deg"
                )
                print(
                    f"Theta from beta = {deg(theta):.6f} deg"
                )

                if abs(theta - theta_given) > rad(0.1):
                    print("WARNING: Supplied theta and beta are inconsistent.")

        elif theta_given is not None:
            roots = find_shock_roots(M1, theta_given, gamma)

            if not roots:
                print("No attached oblique shock solution exists.")
                return None, None

            print("\nPossible beta solutions:")

            if len(roots) == 1:
                beta = roots[0]
                print(f"beta = {deg(beta):.6f} deg")

            else:
                print(f"Weak solution beta = {deg(roots[0]):.6f} deg")
                print(f"Strong solution beta = {deg(roots[-1]):.6f} deg")

                branch = ask_choice(
                    "Choose weak or strong (w/s): ",
                    ["w", "s"]
                )

                beta = roots[0] if branch == "w" else roots[-1]

            theta = theta_from_beta(M1, beta, gamma)

        elif p_ratio_given is not None:
            Mn1_squared = (
                1.0
                + (p_ratio_given - 1.0)
                * (gamma + 1.0) / (2.0 * gamma)
            )

            if Mn1_squared <= 1.0:
                print("Pressure ratio must be greater than 1.")
                return None, None

            Mn1_from_pressure = math.sqrt(Mn1_squared)

            if Mn1_from_pressure > M1:
                print("The supplied pressure ratio is physically impossible.")
                return None, None

            beta = math.asin(Mn1_from_pressure / M1)
            theta = theta_from_beta(M1, beta, gamma)

            print("\nBeta calculated from pressure ratio:")
            print("Mn1^2 = 1 + [(p2/p1 - 1)(gamma+1)]/(2 gamma)")
            print(f"Mn1 = {Mn1_from_pressure:.8f}")
            print("beta = asin(Mn1/M1)")
            print(f"beta = {deg(beta):.6f} deg")
            print(f"theta = {deg(theta):.6f} deg")

        else:
            # Determine beta from downstream Mach number.
            def calculate_M2(beta_value):
                theta_value = theta_from_beta(
                    M1, beta_value, gamma
                )

                Mn1_value = M1 * math.sin(beta_value)

                if Mn1_value <= 1.0:
                    return None

                Mn2_value = normal_mach_downstream(
                    Mn1_value, gamma
                )

                denominator = math.sin(beta_value - theta_value)

                if denominator <= 0:
                    return None

                return Mn2_value / denominator

            beta_min = mu1 + 1e-7
            beta_max = math.pi / 2 - 1e-7

            roots = find_roots(
                lambda b: calculate_M2(b)
                if calculate_M2(b) is not None else 1e12,
                M2_given,
                beta_min,
                beta_max
            )

            if not roots:
                print("No physical beta solution was found for M2.")
                return None, None

            print("\nPossible beta solutions:")

            if len(roots) == 1:
                beta = roots[0]
            else:
                print(f"Weak solution beta = {deg(roots[0]):.6f} deg")
                print(f"Strong solution beta = {deg(roots[-1]):.6f} deg")

                branch = ask_choice(
                    "Choose weak or strong (w/s): ",
                    ["w", "s"]
                )

                beta = roots[0] if branch == "w" else roots[-1]

            theta = theta_from_beta(M1, beta, gamma)

        # ------------------------------------------------------
        # Calculate shock properties
        # ------------------------------------------------------

        Mn1 = M1 * math.sin(beta)

        if Mn1 <= 1.0:
            print("Mn1 must be greater than 1.")
            return None, None

        p_ratio, rho_ratio, T_ratio = shock_ratios(Mn1, gamma)

        Mn2 = normal_mach_downstream(Mn1, gamma)

        M2 = Mn2 / math.sin(beta - theta)

        mu2 = mach_angle(M2)

        p0_ratio = p_ratio * (
            (1.0 + (gamma - 1.0) * M2**2 / 2.0)
            / (1.0 + (gamma - 1.0) * M1**2 / 2.0)
        ) ** (gamma / (gamma - 1.0))

        # ------------------------------------------------------
        # Display solution
        # ------------------------------------------------------

        print("\n========== OBLIQUE SHOCK RESULTS ==========")
        print(f"M1 = {M1:.8f}")
        print(f"Mach angle mu1 = {deg(mu1):.6f} deg")
        print(f"Turning angle theta = {deg(theta):.6f} deg")
        print(f"Shock angle beta = {deg(beta):.6f} deg")
        print(f"Mn1 = {Mn1:.8f}")
        print(f"Mn2 = {Mn2:.8f}")
        print(f"M2 = {M2:.8f}")

        if mu2 is not None:
            print(f"Mach angle mu2 = {deg(mu2):.6f} deg")
        else:
            print("M2 < 1: downstream Mach angle is undefined.")

        print("\n--- Property ratios ---")
        print(f"p2/p1 = {p_ratio:.8f}")
        print(f"rho2/rho1 = {rho_ratio:.8f}")
        print(f"T2/T1 = {T_ratio:.8f}")
        print(f"p02/p01 = {p0_ratio:.8f}")
        print("T02/T01 = 1.00000000")

        print("\n========== STEP-BY-STEP SOLUTION ==========")

        print("\n1. Theta-beta-M relation:")
        print("tan(theta) = 2 cot(beta)[M1^2 sin^2(beta)-1]")
        print("             / [M1^2(gamma+cos(2 beta))+2]")
        print(f"theta = {deg(theta):.8f} deg")

        print("\n2. Upstream normal Mach number:")
        print("Mn1 = M1 sin(beta)")
        print(f"Mn1 = {M1:.8f} * sin({deg(beta):.8f})")
        print(f"Mn1 = {Mn1:.8f}")

        print("\n3. Static pressure ratio:")
        print("p2/p1 = 1 + 2 gamma/(gamma+1)(Mn1^2-1)")
        print(f"p2/p1 = {p_ratio:.8f}")

        print("\n4. Density ratio:")
        print("rho2/rho1 = (gamma+1)Mn1^2/[(gamma-1)Mn1^2+2]")
        print(f"rho2/rho1 = {rho_ratio:.8f}")

        print("\n5. Temperature ratio:")
        print("T2/T1 = (p2/p1)/(rho2/rho1)")
        print(f"T2/T1 = {p_ratio:.8f}/{rho_ratio:.8f}")
        print(f"T2/T1 = {T_ratio:.8f}")

        print("\n6. Downstream normal Mach number:")
        print("Mn2 = sqrt[(1+(gamma-1)Mn1^2/2)")
        print("           /(gamma Mn1^2-(gamma-1)/2)]")
        print(f"Mn2 = {Mn2:.8f}")

        print("\n7. Downstream Mach number:")
        print("M2 = Mn2/sin(beta-theta)")
        print(f"M2 = {Mn2:.8f}/sin({deg(beta-theta):.8f})")
        print(f"M2 = {M2:.8f}")

        print("\n8. Stagnation pressure ratio:")
        print(f"p02/p01 = {p0_ratio:.8f}")
        print("T02/T01 = 1.00000000")

        next_state = {
            "M": M2,
            "p": None,
            "T": None,
            "rho": None,
            "p0": None,
            "T0": state.get("T0"),
            "rho0": None,
            "V": None,
            "a": None
        }

        if state.get("p") is not None:
            next_state["p"] = state["p"] * p_ratio

        if state.get("T") is not None:
            next_state["T"] = state["T"] * T_ratio

        if state.get("rho") is not None:
            next_state["rho"] = state["rho"] * rho_ratio

        if state.get("p0") is not None:
            next_state["p0"] = state["p0"] * p0_ratio

        if state.get("T0") is not None:
            next_state["T0"] = state["T0"]

        next_state = complete_state(next_state)

        result = {
            "type": "Oblique",
            "theta": deg(theta),
            "beta": deg(beta),
            "mu1": deg(mu1),
            "Mn1": Mn1,
            "Mn2": Mn2,
            "mu2": deg(mu2) if mu2 is not None else None,
            "M1": M1,
            "M2": M2
        }

        return next_state, result

    # ----------------------------------------------------------
    # NORMAL SHOCK
    # ----------------------------------------------------------

    def apply_normal_shock(state, layer_number):
        M1 = state.get("M")

        if M1 is None or M1 <= 1.0:
            print("A normal shock requires M1 > 1.")
            return None, None

        print(f"\n========== LAYER {layer_number}: NORMAL SHOCK ==========")

        beta = math.pi / 2.0
        theta = 0.0
        Mn1 = M1

        p_ratio, rho_ratio, T_ratio = shock_ratios(Mn1, gamma)

        Mn2 = normal_mach_downstream(Mn1, gamma)
        M2 = Mn2

        mu1 = mach_angle(M1)
        mu2 = mach_angle(M2)

        p0_ratio = p_ratio * (
            (1.0 + (gamma - 1.0) * M2**2 / 2.0)
            / (1.0 + (gamma - 1.0) * M1**2 / 2.0)
        ) ** (gamma / (gamma - 1.0))

        print("\n========== NORMAL SHOCK RESULTS ==========")
        print(f"M1 = {M1:.8f}")
        print("theta = 0 degrees")
        print("beta = 90 degrees")
        print(f"mu1 = {deg(mu1):.6f} deg")
        print(f"Mn1 = {Mn1:.8f}")
        print(f"Mn2 = {Mn2:.8f}")
        print(f"M2 = {M2:.8f}")

        if mu2 is not None:
            print(f"mu2 = {deg(mu2):.6f} deg")
        else:
            print("M2 < 1: downstream Mach angle is undefined.")

        print("\n--- Property ratios ---")
        print(f"p2/p1 = {p_ratio:.8f}")
        print(f"rho2/rho1 = {rho_ratio:.8f}")
        print(f"T2/T1 = {T_ratio:.8f}")
        print(f"p02/p01 = {p0_ratio:.8f}")
        print("T02/T01 = 1.00000000")

        print("\n========== STEP-BY-STEP SOLUTION ==========")

        print("\n1. Normal shock geometry:")
        print("beta = 90 degrees; theta = 0 degrees")
        print("Mn1 = M1")
        print(f"Mn1 = {M1:.8f}")

        print("\n2. Pressure ratio:")
        print("p2/p1 = 1 + 2 gamma/(gamma+1)(Mn1^2-1)")
        print(f"p2/p1 = {p_ratio:.8f}")

        print("\n3. Density ratio:")
        print("rho2/rho1 = (gamma+1)Mn1^2/[(gamma-1)Mn1^2+2]")
        print(f"rho2/rho1 = {rho_ratio:.8f}")

        print("\n4. Temperature ratio:")
        print("T2/T1 = (p2/p1)/(rho2/rho1)")
        print(f"T2/T1 = {T_ratio:.8f}")

        print("\n5. Downstream normal Mach number:")
        print(f"Mn2 = {Mn2:.8f}")

        print("\n6. Downstream Mach number:")
        print("M2 = Mn2")
        print(f"M2 = {M2:.8f}")

        print("\n7. Stagnation pressure ratio:")
        print(f"p02/p01 = {p0_ratio:.8f}")

        next_state = {
            "M": M2,
            "p": None,
            "T": None,
            "rho": None,
            "p0": None,
            "T0": state.get("T0"),
            "rho0": None,
            "V": None,
            "a": None
        }

        if state.get("p") is not None:
            next_state["p"] = state["p"] * p_ratio

        if state.get("T") is not None:
            next_state["T"] = state["T"] * T_ratio

        if state.get("rho") is not None:
            next_state["rho"] = state["rho"] * rho_ratio

        if state.get("p0") is not None:
            next_state["p0"] = state["p0"] * p0_ratio

        if state.get("T0") is not None:
            next_state["T0"] = state["T0"]

        next_state = complete_state(next_state)

        result = {
            "type": "Normal",
            "theta": 0.0,
            "beta": 90.0,
            "mu1": deg(mu1),
            "Mn1": Mn1,
            "Mn2": Mn2,
            "mu2": deg(mu2) if mu2 is not None else None,
            "M1": M1,
            "M2": M2
        }

        return next_state, result

    # ----------------------------------------------------------
    # EXPANSION FAN
    # ----------------------------------------------------------

    def apply_expansion(state, layer_number):
        M1 = state.get("M")

        if M1 is None or M1 < 1.0:
            print("Expansion requires M1 >= 1.")
            return None, None

        print(f"\n========== LAYER {layer_number}: EXPANSION FAN ==========")

        theta_deg = ask_float(
            "Expansion turning angle theta [degrees]: ",
            minimum=0.0
        )

        theta = rad(theta_deg)

        nu1 = prandtl_meyer(M1, gamma)
        nu2 = nu1 + theta

        M2 = inverse_prandtl_meyer(nu2, gamma)

        if M2 is None:
            print("Expansion angle exceeds the Prandtl-Meyer limit.")
            return None, None

        T_ratio = (
            (1.0 + (gamma - 1.0) * M1**2 / 2.0)
            / (1.0 + (gamma - 1.0) * M2**2 / 2.0)
        )

        p_ratio = T_ratio ** (gamma / (gamma - 1.0))
        rho_ratio = p_ratio / T_ratio

        mu1 = mach_angle(M1)
        mu2 = mach_angle(M2)

        print("\n========== EXPANSION RESULTS ==========")
        print(f"M1 = {M1:.8f}")
        print(f"theta = {theta_deg:.6f} deg")
        print(f"nu1 = {deg(nu1):.6f} deg")
        print(f"nu2 = {deg(nu2):.6f} deg")
        print(f"M2 = {M2:.8f}")
        print(f"mu1 = {deg(mu1):.6f} deg")
        print(f"mu2 = {deg(mu2):.6f} deg")

        print("\n--- Property ratios ---")
        print(f"T2/T1 = {T_ratio:.8f}")
        print(f"p2/p1 = {p_ratio:.8f}")
        print(f"rho2/rho1 = {rho_ratio:.8f}")
        print("p02/p01 = 1.00000000")
        print("T02/T01 = 1.00000000")

        print("\n========== STEP-BY-STEP SOLUTION ==========")

        print("\n1. Mach angle upstream:")
        print("mu1 = asin(1/M1)")
        print(f"mu1 = {deg(mu1):.8f} deg")

        print("\n2. Prandtl-Meyer function:")
        print(f"nu1 = {deg(nu1):.8f} deg")

        print("\n3. Expansion relation:")
        print("nu2 = nu1 + theta")
        print(f"nu2 = {deg(nu1):.8f} + {theta_deg:.8f}")
        print(f"nu2 = {deg(nu2):.8f} deg")

        print("\n4. Invert Prandtl-Meyer function:")
        print(f"M2 = {M2:.8f}")

        print("\n5. Downstream Mach angle:")
        print("mu2 = asin(1/M2)")
        print(f"mu2 = {deg(mu2):.8f} deg")

        print("\n6. Temperature ratio:")
        print("T2/T1 = [1+(gamma-1)M1^2/2]")
        print("        /[1+(gamma-1)M2^2/2]")
        print(f"T2/T1 = {T_ratio:.8f}")

        print("\n7. Pressure ratio:")
        print("p2/p1 = (T2/T1)^[gamma/(gamma-1)]")
        print(f"p2/p1 = {p_ratio:.8f}")

        print("\n8. Density ratio:")
        print("rho2/rho1 = (p2/p1)/(T2/T1)")
        print(f"rho2/rho1 = {rho_ratio:.8f}")

        next_state = {
            "M": M2,
            "p": None,
            "T": None,
            "rho": None,
            "p0": state.get("p0"),
            "T0": state.get("T0"),
            "rho0": state.get("rho0"),
            "V": None,
            "a": None
        }

        if state.get("p") is not None:
            next_state["p"] = state["p"] * p_ratio

        if state.get("T") is not None:
            next_state["T"] = state["T"] * T_ratio

        if state.get("rho") is not None:
            next_state["rho"] = state["rho"] * rho_ratio

        next_state = complete_state(next_state)

        result = {
            "type": "Expansion",
            "theta": theta_deg,
            "beta": None,
            "mu1": deg(mu1),
            "Mn1": None,
            "Mn2": None,
            "mu2": deg(mu2),
            "M1": M1,
            "M2": M2
        }

        return next_state, result

    # ----------------------------------------------------------
    # RESULT TABLES
    # ----------------------------------------------------------

    def display_layer_table(results):
        print("\n\n==================== LAYER RESULTS ====================")

        print(
            f"{'Layer':<7}"
            f"{'Type':<12}"
            f"{'M1':>9}"
            f"{'M2':>9}"
            f"{'theta':>11}"
            f"{'beta':>11}"
            f"{'mu1':>11}"
            f"{'Mn1':>10}"
            f"{'Mn2':>10}"
            f"{'mu2':>11}"
        )

        print("-" * 101)

        for item in results:
            def fmt(value):
                return "N/A" if value is None else f"{value:.4f}"

            print(
                f"{item['layer']:<7}"
                f"{item['type']:<12}"
                f"{fmt(item['M1']):>9}"
                f"{fmt(item['M2']):>9}"
                f"{fmt(item['theta']):>11}"
                f"{fmt(item['beta']):>11}"
                f"{fmt(item['mu1']):>11}"
                f"{fmt(item['Mn1']):>10}"
                f"{fmt(item['Mn2']):>10}"
                f"{fmt(item['mu2']):>11}"
            )

    def display_regions(regions):
        print("\n\n==================== REGION COMPARISON ====================")

        keys = [
            ("M", "Mach M"),
            ("p", "Static p [Pa]"),
            ("p0", "Stagnation p0 [Pa]"),
            ("T", "Static T [K]"),
            ("T0", "Stagnation T0 [K]"),
            ("rho", "Static rho [kg/m3]"),
            ("rho0", "Stagnation rho0 [kg/m3]"),
            ("V", "Velocity V [m/s]"),
            ("a", "Sound speed a [m/s]")
        ]

        header = f"{'Property':<22}"

        for i in range(len(regions)):
            header += f"{('Region ' + str(i + 1)):>17}"

        print(header)
        print("-" * len(header))

        for key, label in keys:
            line = f"{label:<22}"

            for state in regions:
                value = state.get(key)

                if value is None:
                    line += f"{'N/A':>17}"
                else:
                    line += f"{value:>17.6g}"

            print(line)

    # ==========================================================
    # SHOCK INTERACTION SOLVER
    # ==========================================================

    def interaction_wave(M1, p1, theta_deg, wave_type,
                         gamma, branch="w"):

        theta = rad(abs(theta_deg))

        # No additional turning
        if theta < 1e-10:
            return {
                "M": M1,
                "p": p1,
                "theta": 0.0,
                "beta": None,
                "Mn1": None,
                "Mn2": None,
                "type": "No additional wave"
            }

        # ------------------------------------------------------
        # OBLIQUE SHOCK
        # ------------------------------------------------------

        if wave_type == "shock":

            if M1 <= 1.0:
                return None

            roots = find_shock_roots(M1, theta, gamma)

            if not roots:
                return None

            beta = roots[0] if branch == "w" else roots[-1]

            Mn1 = M1 * math.sin(beta)
            Mn2 = normal_mach_downstream(Mn1, gamma)

            denominator = math.sin(beta - theta)

            if denominator <= 0:
                return None

            M2 = Mn2 / denominator

            p_ratio, rho_ratio, T_ratio = shock_ratios(
                Mn1, gamma
            )

            return {
                "M": M2,
                "p": p1 * p_ratio,
                "theta": deg(theta),
                "beta": deg(beta),
                "Mn1": Mn1,
                "Mn2": Mn2,
                "p_ratio": p_ratio,
                "rho_ratio": rho_ratio,
                "T_ratio": T_ratio,
                "type": "Oblique shock"
            }

        # ------------------------------------------------------
        # PRANDTL-MEYER EXPANSION
        # ------------------------------------------------------

        elif wave_type == "expansion":

            if M1 < 1.0:
                return None

            nu1 = prandtl_meyer(M1, gamma)
            nu2 = nu1 + theta

            M2 = inverse_prandtl_meyer(nu2, gamma)

            if M2 is None:
                return None

            T_ratio = (
                (1.0 + (gamma - 1.0) * M1**2 / 2.0)
                /
                (1.0 + (gamma - 1.0) * M2**2 / 2.0)
            )

            p_ratio = T_ratio ** (
                gamma / (gamma - 1.0)
            )

            rho_ratio = p_ratio / T_ratio

            return {
                "M": M2,
                "p": p1 * p_ratio,
                "theta": deg(theta),
                "beta": None,
                "Mn1": None,
                "Mn2": None,
                "p_ratio": p_ratio,
                "rho_ratio": rho_ratio,
                "T_ratio": T_ratio,
                "nu1": deg(nu1),
                "nu2": deg(nu2),
                "type": "Expansion fan"
            }

        return None

    # ==========================================================
    # CREATE THE TWO INCOMING REGIONS
    # ==========================================================

    def create_incoming_region(M1, p1, signed_theta, branch):

        result = interaction_wave(
            M1,
            p1,
            signed_theta,
            "shock",
            gamma,
            branch
        )

        if result is None:
            return None

        result["flow_angle"] = signed_theta

        return result

    # ==========================================================
    # FIND THE COMMON DOWNSTREAM FLOW DIRECTION
    # ==========================================================

    def solve_interaction_direction(region_a, region_b,
                                    wave_a, wave_b,
                                    branch_a, branch_b):

        phi_a = region_a["flow_angle"]
        phi_b = region_b["flow_angle"]

        def pressure_difference(target_angle):

            delta_a = target_angle - phi_a
            delta_b = target_angle - phi_b

            result_a = interaction_wave(
                region_a["M"],
                region_a["p"],
                delta_a,
                wave_a,
                gamma,
                branch_a
            )

            result_b = interaction_wave(
                region_b["M"],
                region_b["p"],
                delta_b,
                wave_b,
                gamma,
                branch_b
            )

            if result_a is None or result_b is None:
                return None

            return result_a["p"] - result_b["p"]

        # Search for a common downstream flow direction.
        # The search interval extends 45 degrees beyond
        # the two incoming flow directions.

        low = min(phi_a, phi_b) - 45.0
        high = max(phi_a, phi_b) + 45.0

        samples = 3000
        roots = []

        previous_x = None
        previous_f = None

        for i in range(samples + 1):

            x = low + (high - low) * i / samples
            f = pressure_difference(x)

            if f is None:
                previous_x = None
                previous_f = None
                continue

            if abs(f) < 1e-9:
                roots.append(x)

            elif previous_f is not None and previous_f * f < 0:

                a = previous_x
                b = x
                fa = previous_f

                # Bisection
                for _ in range(100):

                    middle = (a + b) / 2.0
                    fm = pressure_difference(middle)

                    if fm is None:
                        break

                    if abs(fm) < 1e-10:
                        a = middle
                        b = middle
                        break

                    if fa * fm <= 0:
                        b = middle
                    else:
                        a = middle
                        fa = fm

                root = (a + b) / 2.0

                if not roots or all(
                    abs(root - old) > 1e-5 for old in roots
                ):
                    roots.append(root)

            previous_x = x
            previous_f = f

        if not roots:
            return None

        # If multiple mathematical solutions exist,
        # select the one closest to the mean incoming direction.

        reference = (phi_a + phi_b) / 2.0

        target = min(
            roots,
            key=lambda value: abs(value - reference)
        )

        delta_a = target - phi_a
        delta_b = target - phi_b

        result_a = interaction_wave(
            region_a["M"],
            region_a["p"],
            delta_a,
            wave_a,
            gamma,
            branch_a
        )

        result_b = interaction_wave(
            region_b["M"],
            region_b["p"],
            delta_b,
            wave_b,
            gamma,
            branch_b
        )

        return {
            "target": target,
            "region_a": result_a,
            "region_b": result_b,
            "delta_a": delta_a,
            "delta_b": delta_b,
            "roots": roots
        }

    # ==========================================================
    # DISPLAY INTERACTION RESULTS
    # ==========================================================

    def display_interaction_results(incoming_a, incoming_b,
                                    solution, label_a, label_b):

        a = solution["region_a"]
        b = solution["region_b"]

        print("\n==============================================")
        print("           INTERACTION RESULTS")
        print("==============================================")

        print("\n--- Incoming regions ---")

        print(
            f"Region A: M = {incoming_a['M']:.6f}, "
            f"p = {incoming_a['p']:.6f}, "
            f"flow angle = {incoming_a['flow_angle']:+.6f} deg"
        )

        print(
            f"Region B: M = {incoming_b['M']:.6f}, "
            f"p = {incoming_b['p']:.6f}, "
            f"flow angle = {incoming_b['flow_angle']:+.6f} deg"
        )

        print("\n--- Outgoing waves ---")

        print(f"\n{label_a}")
        print(f"Wave type: {a['type']}")
        print(f"Turning magnitude = {a['theta']:.6f} deg")
        print(f"M downstream = {a['M']:.8f}")
        print(f"Pressure ratio = {a['p_ratio']:.8f}")

        if a["beta"] is not None:
            print(f"Beta = {a['beta']:.6f} deg")
            print(f"Mn1 = {a['Mn1']:.8f}")
            print(f"Mn2 = {a['Mn2']:.8f}")

        print(f"\n{label_b}")
        print(f"Wave type: {b['type']}")
        print(f"Turning magnitude = {b['theta']:.6f} deg")
        print(f"M downstream = {b['M']:.8f}")
        print(f"Pressure ratio = {b['p_ratio']:.8f}")

        if b["beta"] is not None:
            print(f"Beta = {b['beta']:.6f} deg")
            print(f"Mn1 = {b['Mn1']:.8f}")
            print(f"Mn2 = {b['Mn2']:.8f}")

        print("\n--- Slip-line compatibility ---")

        print(
            f"Common flow direction = "
            f"{solution['target']:+.8f} deg"
        )

        print(f"Pressure in region 4 = {a['p']:.8f}")
        print(f"Pressure in region 4' = {b['p']:.8f}")

        print(
            f"Pressure difference = "
            f"{abs(a['p'] - b['p']):.10e}"
        )

        print("Downstream flow directions are parallel.")
        print("Slip-line direction = common downstream direction.")

        print("\nNote:")
        print("The two downstream velocity magnitudes")
        print("and other thermodynamic properties may differ.")
        print("Pressure is normalized to freestream pressure")
        print("if no absolute freestream pressure was supplied.")

    # ==========================================================
    # OPPOSING-WAVE INTERACTION - FIGURE 9.21
    # ==========================================================

    def opposing_interaction(initial_state):

        print("\n========== OPPOSING SHOCK INTERACTION ==========")

        M1 = initial_state["M"]

        if M1 <= 1.0:
            print("The incoming flow must be supersonic.")
            return

        p1 = initial_state.get("p")
        if p1 is None:
            p1 = 1.0
            print("No absolute p1 supplied. Using p1 = 1.0.")

        print("\nEnter signed incoming flow deflections.")
        print("Positive = upward; negative = downward.")

        theta_a = ask_float(
            "Incoming shock A deflection [degrees]: "
        )

        theta_b = ask_float(
            "Incoming shock B deflection [degrees]: "
        )

        if theta_a * theta_b >= 0:
            print("For opposing interaction, use opposite signs.")
            return

        print("\nIncoming shock branch:")
        branch = ask_choice(
            "[w] Weak or [s] Strong: ",
            ["w", "s"]
        )

        region_a = create_incoming_region(
            M1, p1, theta_a, branch
        )

        region_b = create_incoming_region(
            M1, p1, theta_b, branch
        )

        if region_a is None or region_b is None:
            print("An incoming shock has no attached solution.")
            return

        print("\nIncoming shock results:")
        print(
            f"Region A: M2 = {region_a['M']:.8f}, "
            f"p2/p1 = {region_a['p'] / p1:.8f}"
        )
        print(
            f"Region B: M3 = {region_b['M']:.8f}, "
            f"p3/p1 = {region_b['p'] / p1:.8f}"
        )

        print("\nOutgoing refracted waves are treated as shocks.")

        outgoing_branch = ask_choice(
            "Outgoing shock branch [w/s]: ",
            ["w", "s"]
        )

        solution = solve_interaction_direction(
            region_a,
            region_b,
            "shock",
            "shock",
            outgoing_branch,
            outgoing_branch
        )

        if solution is None:
            print("\nNo regular opposing-shock interaction solution found.")
            print("The specified waves cannot satisfy both compatibility")
            print("conditions using the selected shock branches.")
            return

        display_interaction_results(
            region_a,
            region_b,
            solution,
            "Refracted shock D",
            "Refracted shock C"
        )

    # ==========================================================
    # SAME-DIRECTION WAVE INTERACTION - FIGURE 9.22
    # ==========================================================

    def same_direction_interaction(initial_state):

        print("\n========== SAME-DIRECTION WAVE INTERACTION ==========")

        M1 = initial_state["M"]

        if M1 <= 1.0:
            print("The incoming flow must be supersonic.")
            return

        p1 = initial_state.get("p")
        if p1 is None:
            p1 = 1.0
            print("No absolute p1 supplied. Using p1 = 1.0.")

        print("\nEnter signed incoming flow deflections.")
        print("Positive = upward; negative = downward.")

        theta_a = ask_float(
            "Incoming shock A deflection [degrees]: "
        )

        theta_b = ask_float(
            "Incoming shock B deflection [degrees]: "
        )

        branch_in = ask_choice(
            "Incoming shock branch [w/s]: ",
            ["w", "s"]
        )

        region_a = create_incoming_region(
            M1, p1, theta_a, branch_in
        )

        region_b = create_incoming_region(
            M1, p1, theta_b, branch_in
        )

        if region_a is None or region_b is None:
            print("An incoming shock has no attached solution.")
            return

        print("\nOutgoing wave types:")
        print("[1] Transmitted shock + reflected shock")
        print("[2] Transmitted shock + reflected expansion")

        mode = ask_choice("Select: ", ["1", "2"])

        reflected_type = (
            "shock" if mode == "1" else "expansion"
        )

        transmitted_branch = ask_choice(
            "Transmitted shock branch [w/s]: ",
            ["w", "s"]
        )

        reflected_branch = "w"

        if reflected_type == "shock":
            reflected_branch = ask_choice(
                "Reflected shock branch [w/s]: ",
                ["w", "s"]
            )

        solution = solve_interaction_direction(
            region_a,
            region_b,
            "shock",
            reflected_type,
            transmitted_branch,
            reflected_branch
        )

        if solution is None:
            print("\nNo regular interaction solution found.")
            print("Pressure and flow-direction compatibility")
            print("could not both be satisfied for these inputs.")
            return

        display_interaction_results(
            region_a,
            region_b,
            solution,
            "Transmitted wave CD",
            "Reflected wave CE"
        )
    
    # ==========================================================
    # AIRFOIL CALCULATIONS - CHAPTER 9
    # ==========================================================

    def airfoil_shock(M1, theta_deg, gamma):
        """Weak attached oblique-shock solution for an airfoil panel."""

        if M1 <= 1.0:
            raise ValueError("Oblique shock requires M1 > 1.")

        if theta_deg <= 0:
            raise ValueError("Shock turning angle must be positive.")

        theta = math.radians(theta_deg)
        roots = find_shock_roots(M1, theta, gamma)

        if not roots:
            raise ValueError(
                f"No attached shock solution for M={M1:.5f}, "
                f"theta={theta_deg:.5f} deg."
            )

        # Use the weak-shock branch.
        beta = roots[0]

        Mn1 = M1 * math.sin(beta)
        Mn2 = normal_mach_downstream(Mn1, gamma)

        p_ratio, rho_ratio, T_ratio = shock_ratios(Mn1, gamma)

        M2 = Mn2 / math.sin(beta - theta)

        p0_ratio = p_ratio * (
            (1.0 + (gamma - 1.0) * M2**2 / 2.0)
            / (1.0 + (gamma - 1.0) * M1**2 / 2.0)
        ) ** (gamma / (gamma - 1.0))

        return {
            "type": "Oblique shock",
            "M1": M1,
            "M2": M2,
            "theta": theta_deg,
            "beta": math.degrees(beta),
            "Mn1": Mn1,
            "Mn2": Mn2,
            "p_ratio": p_ratio,
            "rho_ratio": rho_ratio,
            "T_ratio": T_ratio,
            "p0_ratio": p0_ratio
        }

    def airfoil_expansion(M1, theta_deg, gamma):
        """Prandtl-Meyer expansion solution for an airfoil panel."""

        if M1 < 1.0:
            raise ValueError("Expansion requires M1 >= 1.")

        if theta_deg < 0:
            raise ValueError("Expansion angle cannot be negative.")

        theta = math.radians(theta_deg)

        nu1 = prandtl_meyer(M1, gamma)
        nu2 = nu1 + theta

        M2 = inverse_prandtl_meyer(nu2, gamma)

        if M2 is None:
            raise ValueError("Expansion angle exceeds the PM limit.")

        T_ratio = (
            (1.0 + (gamma - 1.0) * M1**2 / 2.0)
            / (1.0 + (gamma - 1.0) * M2**2 / 2.0)
        )

        p_ratio = T_ratio ** (gamma / (gamma - 1.0))
        rho_ratio = p_ratio / T_ratio

        return {
            "type": "Expansion",
            "M1": M1,
            "M2": M2,
            "theta": theta_deg,
            "beta": None,
            "Mn1": None,
            "Mn2": None,
            "p_ratio": p_ratio,
            "rho_ratio": rho_ratio,
            "T_ratio": T_ratio,
            "p0_ratio": 1.0
        }


    def display_airfoil_wave(name, wave, p_upstream, p_downstream):

        print(f"\n========== {name} ==========")
        print(f"Wave type = {wave['type']}")

        M1 = wave["M1"]
        M2 = wave["M2"]
        theta_deg = wave["theta"]
        theta_rad = math.radians(theta_deg)

        print("\n1. Upstream and downstream Mach numbers:")
        print(f"M1 = {M1:.8f}")
        print(f"M2 = {M2:.8f}")
        print(f"Flow turning = {theta_deg:.8f} deg")

        if wave["type"] == "Oblique shock":

            beta_deg = wave["beta"]
            beta = math.radians(beta_deg)

            print("\n2. Theta-beta-M equation:")
            print(
                "tan(theta) = 2*cot(beta)*"
                "(M1^2*sin^2(beta)-1) / "
                "(M1^2*(gamma+cos(2*beta))+2)"
            )
            print("Weak attached-shock solution selected.")
            print(f"beta = {beta_deg:.8f} deg")

            print("\n3. Upstream normal Mach number:")
            print("Mn1 = M1 * sin(beta)")
            print(
                f"Mn1 = {M1:.8f} * sin({beta_deg:.8f})"
            )
            print(f"Mn1 = {wave['Mn1']:.8f}")

            print("\n4. Downstream normal Mach number:")
            print(
                "Mn2 = sqrt((1+(gamma-1)*Mn1^2/2) / "
                "(gamma*Mn1^2-(gamma-1)/2))"
            )
            print(f"Mn2 = {wave['Mn2']:.8f}")

            print("\n5. Static pressure ratio:")
            print(
                "p2/p1 = 1 + 2*gamma/(gamma+1)*(Mn1^2-1)"
            )
            print(f"p2/p1 = {wave['p_ratio']:.8f}")

            print("\n6. Density ratio:")
            print(
                "rho2/rho1 = (gamma+1)*Mn1^2 / "
                "((gamma-1)*Mn1^2+2)"
            )
            print(f"rho2/rho1 = {wave['rho_ratio']:.8f}")

            print("\n7. Temperature ratio:")
            print("T2/T1 = (p2/p1)/(rho2/rho1)")
            print(f"T2/T1 = {wave['T_ratio']:.8f}")

            print("\n8. Downstream Mach number:")
            print("M2 = Mn2 / sin(beta-theta)")
            print(f"M2 = {M2:.8f}")

            print("\n9. Stagnation pressure ratio:")
            print("p02/p01 = (p2/p1) *")
            print(
                "[(1+(gamma-1)*M2^2/2) / "
                "(1+(gamma-1)*M1^2/2)]"
                "^[gamma/(gamma-1)]"
            )
            print(f"p02/p01 = {wave['p0_ratio']:.8f}")

        elif wave["type"] == "Expansion":

            nu1 = prandtl_meyer(M1, gamma_airfoil)
            nu2 = nu1 + theta_rad

            print("\n2. Prandtl-Meyer equation:")
            print(
                "nu = sqrt((gamma+1)/(gamma-1))*"
                "atan(sqrt((gamma-1)/(gamma+1)*(M^2-1)))"
                " - atan(sqrt(M^2-1))"
            )

            print("\n3. Initial Prandtl-Meyer angle:")
            print(f"nu1 = {math.degrees(nu1):.8f} deg")

            print("\n4. Final Prandtl-Meyer angle:")
            print("nu2 = nu1 + theta")
            print(
                f"nu2 = {math.degrees(nu1):.8f} "
                f"+ {theta_deg:.8f}"
            )
            print(f"nu2 = {math.degrees(nu2):.8f} deg")

            print("\n5. Inverse Prandtl-Meyer solution:")
            print("M2 = nu_inverse(nu2, gamma)")
            print(f"M2 = {M2:.8f}")

            print("\n6. Temperature ratio:")
            print(
                "T2/T1 = (1+(gamma-1)*M1^2/2) / "
                "(1+(gamma-1)*M2^2/2)"
            )
            print(f"T2/T1 = {wave['T_ratio']:.8f}")

            print("\n7. Pressure ratio:")
            print("p2/p1 = (T2/T1)^[gamma/(gamma-1)]")
            print(f"p2/p1 = {wave['p_ratio']:.8f}")

            print("\n8. Density ratio:")
            print("rho2/rho1 = (p2/p1)/(T2/T1)")
            print(f"rho2/rho1 = {wave['rho_ratio']:.8f}")

            print("\n9. Stagnation pressure:")
            print("p02/p01 = 1.0 (isentropic expansion)")
            print(f"p02/p01 = {wave['p0_ratio']:.8f}")

        else:
            print("\nNo wave occurs because the turning angle is zero.")
            print("All flow properties remain unchanged.")

        print("\n10. Absolute static pressures:")

        print("p_downstream = p_upstream * (p2/p1)")
        print(
            f"p_downstream = {p_upstream:.8f} * "
            f"{wave['p_ratio']:.8f}"
        )
        print(f"p_downstream = {p_downstream:.8f} Pa")

    def airfoil_common_inputs():
        print("\n========== AIRFOIL INPUT DATA ==========")

        gamma_airfoil = ask_float(
            "Specific heat ratio gamma [1.4]: ",
            default=1.4,
            minimum=1.0
        )

        M_inf = ask_float(
            "Freestream Mach number M_inf: ",
            minimum=1.0
        )

        p_inf = ask_float(
            "Freestream static pressure p_inf [Pa]: ",
            minimum=0.0
        )

        chord = ask_float(
            "Airfoil chord c [m]: ",
            minimum=0.0
        )

        span = ask_float(
            "Airfoil span b [m]: ",
            minimum=0.0
        )

        alpha_deg = ask_float(
            "Angle of attack alpha [degrees]: "
        )

        return gamma_airfoil, M_inf, p_inf, chord, span, alpha_deg

    # ----------------------------------------------------------
    # FLAT-PLATE AIRFOIL
    # ----------------------------------------------------------

    def flat_plate_airfoil():
        print("\n========== FLAT-PLATE AIRFOIL ==========")

        (
            gamma_airfoil,
            M_inf,
            p_inf,
            chord,
            span,
            alpha_deg
        ) = airfoil_common_inputs()

        alpha = abs(alpha_deg)

        if alpha >= 90.0:
            print("This flat-plate model requires |alpha| < 90 degrees.")
            return

        if alpha < 1e-10:
            p_upper = p_inf
            p_lower = p_inf
            upper_wave = None
            lower_wave = None

        else:
            expansion = airfoil_expansion(
                M_inf, alpha, gamma_airfoil
            )

            shock = airfoil_shock(
                M_inf, alpha, gamma_airfoil
            )

            if alpha_deg >= 0:
                # Positive alpha:
                # Upper surface = expansion
                # Lower surface = oblique shock
                upper_wave = expansion
                lower_wave = shock
            else:
                # Negative alpha: exchange the two surfaces.
                upper_wave = shock
                lower_wave = expansion

            p_upper = p_inf * upper_wave["p_ratio"]
            p_lower = p_inf * lower_wave["p_ratio"]

        delta_p = p_lower - p_upper

        alpha_rad = math.radians(alpha)

        # Anderson flat-plate pressure-force relations.
        resultant_per_span = delta_p * chord

        lift_per_span = (
            resultant_per_span * math.cos(alpha_rad)
        )

        drag_per_span = (
            abs(resultant_per_span) * math.sin(alpha_rad)
        )

        # Preserve the sign of lift for negative angle of attack.
        lift_per_span *= 1.0 if alpha_deg >= 0 else -1.0

        lift_total = lift_per_span * span
        drag_total = drag_per_span * span

        reference_area = chord * span
        q_inf = 0.5 * gamma_airfoil * p_inf * M_inf**2

        CL = lift_total / (q_inf * reference_area)
        CD = drag_total / (q_inf * reference_area)

        print("\n========== FLAT-PLATE PRESSURES ==========")

        print(f"Freestream pressure p_inf = {p_inf:.6f} Pa")
        print(f"Upper surface pressure    = {p_upper:.6f} Pa")
        print(f"Lower surface pressure    = {p_lower:.6f} Pa")
        print(f"Pressure difference       = {delta_p:.6f} Pa")

        if upper_wave is not None:
            display_airfoil_wave(
                "UPPER SURFACE",
                upper_wave,
                p_inf,
                p_upper
            )

            display_airfoil_wave(
                "LOWER SURFACE",
                lower_wave,
                p_inf,
                p_lower
            )

        print("\n========== FLAT-PLATE FORCE CALCULATION ==========")

        print("\n1. Resultant pressure force per unit span:")
        print("R' = (p_lower - p_upper)c")
        print(
            f"R' = ({p_lower:.6f} - {p_upper:.6f})"
            f" * {chord:.6f}"
        )
        print(f"R' = {resultant_per_span:.6f} N/m")

        print("\n2. Lift per unit span:")
        print("L' = R' cos(alpha)")
        print(f"L' = {lift_per_span:.6f} N/m")

        print("\n3. Drag per unit span:")
        print("D' = |R'| sin(|alpha|)")
        print(f"D' = {drag_per_span:.6f} N/m")

        print("\n4. Total forces:")
        print("L = L' * span")
        print(f"L = {lift_total:.6f} N")
        print("D = D' * span")
        print(f"D = {drag_total:.6f} N")

        print("\n5. Dynamic pressure:")
        print("q_inf = 0.5 gamma p_inf M_inf^2")
        print(f"q_inf = {q_inf:.6f} Pa")

        print("\n6. Reference area:")
        print("S = chord * span")
        print(f"S = {reference_area:.6f} m^2")

        print("\n7. Lift coefficient:")
        print("CL = L / (q_inf S)")
        print(f"CL = {CL:.8f}")

        print("\n8. Drag coefficient:")
        print("CD = D / (q_inf S)")
        print(f"CD = {CD:.8f}")

        print("\n9. Lift-to-drag ratio:")
        if abs(CD) > 1e-12:
            print(f"L/D = {CL / CD:.8f}")
        else:
            print("L/D is undefined because CD is zero.")

        print("\nReference check:")
        print("CD/CL = tan(|alpha|), when CL is positive.")

    # ----------------------------------------------------------
    # DIAMOND AIRFOIL
    # ----------------------------------------------------------

    def diamond_airfoil():
        print("\n========== DIAMOND AIRFOIL ==========")

        (
            gamma_airfoil,
            M_inf,
            p_inf,
            chord,
            span,
            alpha_deg
        ) = airfoil_common_inputs()

        thickness = ask_float(
            "Maximum diamond thickness t [m]: ",
            minimum=0.0
        )

        epsilon_deg = math.degrees(
            math.atan(thickness / chord)
        )

        if abs(alpha_deg) >= epsilon_deg:
            print(
                "\nThis version requires |alpha| < epsilon "
                "so both leading-edge waves are compressive shocks."
            )
            print(f"epsilon = {epsilon_deg:.6f} deg")
            return

        # Positive alpha makes the lower leading-edge shock stronger.
        upper_turn = epsilon_deg - alpha_deg
        lower_turn = epsilon_deg + alpha_deg

        upper_front = airfoil_shock(
            M_inf, upper_turn, gamma_airfoil
        )

        lower_front = airfoil_shock(
            M_inf, lower_turn, gamma_airfoil
        )

        # Pressure and Mach number after the leading-edge shocks.
        M_upper_front = upper_front["M2"]
        M_lower_front = lower_front["M2"]

        p_upper_front = (
            p_inf * upper_front["p_ratio"]
        )

        p_lower_front = (
            p_inf * lower_front["p_ratio"]
        )

        # At the middle corner, each flow expands through 2 epsilon.
        rear_turn = 2.0 * epsilon_deg

        upper_rear = airfoil_expansion(
            M_upper_front, rear_turn, gamma_airfoil
        )

        lower_rear = airfoil_expansion(
            M_lower_front, rear_turn, gamma_airfoil
        )

        p_upper_rear = (
            p_upper_front * upper_rear["p_ratio"]
        )

        p_lower_rear = (
            p_lower_front * lower_rear["p_ratio"]
        )

        print("\n========== DIAMOND AIRFOIL GEOMETRY ==========")
        print(f"Chord c                 = {chord:.6f} m")
        print(f"Maximum thickness t     = {thickness:.6f} m")
        print(f"Half-angle epsilon      = {epsilon_deg:.6f} deg")
        print(f"Angle of attack alpha   = {alpha_deg:.6f} deg")
        print(f"Upper leading turn      = {upper_turn:.6f} deg")
        print(f"Lower leading turn      = {lower_turn:.6f} deg")
        print(f"Rear expansion turn     = {rear_turn:.6f} deg")

        display_airfoil_wave(
            "UPPER FRONT PANEL",
            upper_front,
            p_inf,
            p_upper_front
        )

        display_airfoil_wave(
            "UPPER REAR PANEL",
            upper_rear,
            p_upper_front,
            p_upper_rear
        )

        display_airfoil_wave(
            "LOWER FRONT PANEL",
            lower_front,
            p_inf,
            p_lower_front
        )

        display_airfoil_wave(
            "LOWER REAR PANEL",
            lower_rear,
            p_lower_front,
            p_lower_rear
        )

        # ------------------------------------------------------
        # Pressure-force integration over the four panels.
        #
        # Vertices are ordered clockwise:
        # LE -> upper midpoint -> TE -> lower midpoint -> LE.
        #
        # For each panel:
        # Fx = (p - p_inf) * dy
        # Fy = -(p - p_inf) * dx
        # ------------------------------------------------------

        half_chord = chord / 2.0
        half_thickness = thickness / 2.0

        panels = [
            (
                "Upper front",
                0.0,
                0.0,
                half_chord,
                half_thickness,
                p_upper_front
            ),
            (
                "Upper rear",
                half_chord,
                half_thickness,
                chord,
                0.0,
                p_upper_rear
            ),
            (
                "Lower rear",
                chord,
                0.0,
                half_chord,
                -half_thickness,
                p_lower_rear
            ),
            (
                "Lower front",
                half_chord,
                -half_thickness,
                0.0,
                0.0,
                p_lower_front
            )
        ]

        Fx_per_span = 0.0
        Fy_per_span = 0.0

        print("\n========== PANEL PRESSURE FORCES ==========")
        print(
            f"{'Panel':<16}"
            f"{'Pressure [Pa]':>17}"
            f"{'Fx [N/m]':>15}"
            f"{'Fy [N/m]':>15}"
        )

        for (
            name,
            x1,
            y1,
            x2,
            y2,
            panel_pressure
        ) in panels:

            dx = x2 - x1
            dy = y2 - y1

            gauge_pressure = panel_pressure - p_inf

            Fx_panel = gauge_pressure * dy
            Fy_panel = -gauge_pressure * dx

            Fx_per_span += Fx_panel
            Fy_per_span += Fy_panel

            print(
                f"{name:<16}"
                f"{panel_pressure:>17.6f}"
                f"{Fx_panel:>15.6f}"
                f"{Fy_panel:>15.6f}"
            )

        # Resolve the resultant force into freestream axes.
        alpha_rad = math.radians(alpha_deg)

        drag_per_span = (
            Fx_per_span * math.cos(alpha_rad)
            - Fy_per_span * math.sin(alpha_rad)
        )

        lift_per_span = (
            Fx_per_span * math.sin(alpha_rad)
            + Fy_per_span * math.cos(alpha_rad)
        )


    def diamond_airfoil():
        print("\n========== DIAMOND AIRFOIL ==========")
        print("Anderson Chapter 9 - Shock / Expansion Method")

        # ------------------------------------------------------
        # STEP 1: INPUT DATA
        # ------------------------------------------------------

        gamma_airfoil = 1.4

        print("\n========== STEP 1: GIVEN DATA ==========")
        print(f"Specific heat ratio gamma = {gamma_airfoil:.4f}")

        chord = ask_float(
            "Airfoil chord c [m]: ",
            minimum=0.0
        )

        M_inf = ask_float(
            "Freestream Mach number M_inf: ",
            minimum=1.0
        )

        p_inf = ask_float(
            "Freestream static pressure p_inf [Pa]: ",
            minimum=0.0
        )

        epsilon_deg = ask_float(
            "Diamond half-angle epsilon [degrees]: ",
            minimum=0.0
        )

        alpha_deg = ask_float(
            "Angle of attack alpha [degrees]: "
        )

        if epsilon_deg >= 89.0:
            print("Invalid airfoil angle.")
            return

        gamma = gamma_airfoil

        # ------------------------------------------------------
        # STEP 2: AIRFOIL GEOMETRY
        # ------------------------------------------------------

        epsilon = math.radians(epsilon_deg)
        alpha = math.radians(alpha_deg)

        thickness = chord * math.tan(epsilon)
        half_chord = chord / 2.0
        half_thickness = thickness / 2.0

        print("\n========== STEP 2: AIRFOIL GEOMETRY ==========")
        print("Maximum thickness:")
        print("t = c * tan(epsilon)")
        print(
            f"t = {chord:.6f} * tan({epsilon_deg:.6f})"
        )
        print(f"t = {thickness:.8f} m")

        print("\nHalf chord:")
        print("c/2 = c / 2")
        print(f"c/2 = {half_chord:.8f} m")

        print("\nHalf thickness:")
        print("t/2 = t / 2")
        print(f"t/2 = {half_thickness:.8f} m")

        print("\nAirfoil surface angles:")
        print(f"Upper surface angle = +{epsilon_deg:.6f} deg")
        print(f"Lower surface angle = -{epsilon_deg:.6f} deg")

        # ------------------------------------------------------
        # STEP 3: FREESTREAM PROPERTIES
        # ------------------------------------------------------

        q_inf = 0.5 * gamma * p_inf * M_inf**2

        p0_ratio_inf = (
            1.0 + (gamma - 1.0) * M_inf**2 / 2.0
        ) ** (gamma / (gamma - 1.0))

        p0_inf = p_inf * p0_ratio_inf

        print("\n========== STEP 3: FREESTREAM ==========")

        print("\nDynamic pressure:")
        print("q_inf = 1/2 * gamma * p_inf * M_inf^2")
        print(
            f"q_inf = 0.5 * {gamma:.6f} * "
            f"{p_inf:.6f} * {M_inf:.6f}^2"
        )
        print(f"q_inf = {q_inf:.8f} Pa")

        print("\nFreestream stagnation pressure:")
        print("p0_inf/p_inf = [1 + (gamma-1)M_inf^2/2]"
              "^[gamma/(gamma-1)]")
        print(f"p0_inf/p_inf = {p0_ratio_inf:.8f}")
        print("p0_inf = p_inf * (p0_inf/p_inf)")
        print(f"p0_inf = {p0_inf:.8f} Pa")

        # ------------------------------------------------------
        # STEP 4: LEADING-EDGE FLOW TURNS
        # ------------------------------------------------------

        upper_turn = epsilon_deg - alpha_deg
        lower_turn = epsilon_deg + alpha_deg

        rear_turn = 2.0 * epsilon_deg

        print("\n========== STEP 4: FLOW TURNING ANGLES ==========")

        print("\nUpper leading edge:")
        print("theta_upper = epsilon - alpha")
        print(
            f"theta_upper = {epsilon_deg:.6f} "
            f"- ({alpha_deg:.6f})"
        )
        print(f"theta_upper = {upper_turn:.6f} deg")

        print("\nLower leading edge:")
        print("theta_lower = epsilon + alpha")
        print(
            f"theta_lower = {epsilon_deg:.6f} "
            f"+ ({alpha_deg:.6f})"
        )
        print(f"theta_lower = {lower_turn:.6f} deg")

        print("\nRear-corner turning:")
        print("theta_rear = 2 * epsilon")
        print(
            f"theta_rear = 2 * {epsilon_deg:.6f}"
        )
        print(f"theta_rear = {rear_turn:.6f} deg")

        # ------------------------------------------------------
        # STEP 5: CALCULATE LEADING-EDGE WAVES
        # Positive turn = shock
        # Negative turn = expansion
        # ------------------------------------------------------

        def signed_wave(M1, signed_turn, gamma):
            if abs(signed_turn) < 1e-10:
                return {
                    "type": "No turning",
                    "M1": M1,
                    "M2": M1,
                    "theta": 0.0,
                    "beta": None,
                    "Mn1": None,
                    "Mn2": None,
                    "p_ratio": 1.0,
                    "rho_ratio": 1.0,
                    "T_ratio": 1.0,
                    "p0_ratio": 1.0
                }

            if signed_turn > 0:
                return airfoil_shock(
                    M1, signed_turn, gamma
                )

            return airfoil_expansion(
                M1, abs(signed_turn), gamma
            )

        upper_front = signed_wave(
            M_inf, upper_turn, gamma
        )

        lower_front = signed_wave(
            M_inf, lower_turn, gamma
        )

        M_upper_front = upper_front["M2"]
        M_lower_front = lower_front["M2"]

        p_upper_front = (
            p_inf * upper_front["p_ratio"]
        )

        p_lower_front = (
            p_inf * lower_front["p_ratio"]
        )

        print("\n========== STEP 5: LEADING-EDGE RESULTS ==========")

        display_airfoil_wave(
            "UPPER FRONT PANEL",
            upper_front,
            p_inf,
            p_upper_front
        )

        display_airfoil_wave(
            "LOWER FRONT PANEL",
            lower_front,
            p_inf,
            p_lower_front
        )

        # ------------------------------------------------------
        # STEP 6: REAR-CORNER EXPANSIONS
        # ------------------------------------------------------

        upper_rear = airfoil_expansion(
            M_upper_front,
            rear_turn,
            gamma
        )

        lower_rear = airfoil_expansion(
            M_lower_front,
            rear_turn,
            gamma
        )

        p_upper_rear = (
            p_upper_front * upper_rear["p_ratio"]
        )

        p_lower_rear = (
            p_lower_front * lower_rear["p_ratio"]
        )

        print("\n========== STEP 6: REAR EXPANSIONS ==========")

        display_airfoil_wave(
            "UPPER REAR PANEL",
            upper_rear,
            p_upper_front,
            p_upper_rear
        )

        display_airfoil_wave(
            "LOWER REAR PANEL",
            lower_rear,
            p_lower_front,
            p_lower_rear
        )

        # ------------------------------------------------------
        # STEP 7: PANEL PRESSURES
        # ------------------------------------------------------

        print("\n========== STEP 7: PANEL PRESSURES ==========")

        panels = [
            ("Upper front", p_upper_front,
             0.0, 0.0, half_chord, half_thickness),

            ("Upper rear", p_upper_rear,
             half_chord, half_thickness, chord, 0.0),

            ("Lower rear", p_lower_rear,
             chord, 0.0, half_chord, -half_thickness),

            ("Lower front", p_lower_front,
             half_chord, -half_thickness, 0.0, 0.0)
        ]

        print(f"Freestream pressure = {p_inf:.8f} Pa")
        print("\nPanel pressure summary:")

        for name, pressure, x1, y1, x2, y2 in panels:
            print(
                f"{name:<15} = {pressure:.8f} Pa"
            )

        # ------------------------------------------------------
        # STEP 8: PRESSURE FORCE ON EACH PANEL
        # ------------------------------------------------------

        Fx_per_span = 0.0
        Fy_per_span = 0.0

        print("\n========== STEP 8: PANEL PRESSURE FORCES ==========")

        print("For each panel:")
        print("Delta p = p_panel - p_inf")
        print("Fx' = Delta p * dy")
        print("Fy' = -Delta p * dx")

        for name, pressure, x1, y1, x2, y2 in panels:

            dx = x2 - x1
            dy = y2 - y1

            gauge_pressure = pressure - p_inf

            Fx_panel = gauge_pressure * dy
            Fy_panel = -gauge_pressure * dx

            Fx_per_span += Fx_panel
            Fy_per_span += Fy_panel

            print(f"\n--- {name} ---")
            print(f"x1 = {x1:.8f} m")
            print(f"y1 = {y1:.8f} m")
            print(f"x2 = {x2:.8f} m")
            print(f"y2 = {y2:.8f} m")
            print(f"dx = {dx:.8f} m")
            print(f"dy = {dy:.8f} m")

            print(f"Panel pressure = {pressure:.8f} Pa")
            print(
                f"Gauge pressure = {pressure:.8f} "
                f"- {p_inf:.8f}"
            )
            print(f"Delta p = {gauge_pressure:.8f} Pa")

            print("Fx' = Delta p * dy")
            print(
                f"Fx' = {gauge_pressure:.8f} "
                f"* {dy:.8f}"
            )
            print(f"Fx' = {Fx_panel:.8f} N/m")

            print("Fy' = -Delta p * dx")
            print(
                f"Fy' = -({gauge_pressure:.8f}) "
                f"* {dx:.8f}"
            )
            print(f"Fy' = {Fy_panel:.8f} N/m")

        print("\nTotal body-axis forces per unit span:")
        print(f"Fx' = {Fx_per_span:.8f} N/m")
        print(f"Fy' = {Fy_per_span:.8f} N/m")

        # ------------------------------------------------------
        # STEP 9: RESOLVE FORCES INTO FREESTREAM AXES
        # ------------------------------------------------------

        drag_per_span = (
            Fx_per_span * math.cos(alpha)
            - Fy_per_span * math.sin(alpha)
        )

        lift_per_span = (
            Fx_per_span * math.sin(alpha)
            + Fy_per_span * math.cos(alpha)
        )

        print("\n========== STEP 9: LIFT AND DRAG ==========")

        print("\nDrag per unit span:")
        print("D' = Fx' cos(alpha) - Fy' sin(alpha)")
        print(
            f"D' = {Fx_per_span:.8f} * cos({alpha_deg:.8f})"
            f" - ({Fy_per_span:.8f}) * sin({alpha_deg:.8f})"
        )
        print(f"D' = {drag_per_span:.8f} N/m")

        print("\nLift per unit span:")
        print("L' = Fx' sin(alpha) + Fy' cos(alpha)")
        print(
            f"L' = {Fx_per_span:.8f} * sin({alpha_deg:.8f})"
            f" + {Fy_per_span:.8f} * cos({alpha_deg:.8f})"
        )
        print(f"L' = {lift_per_span:.8f} N/m")

        # ------------------------------------------------------
        # STEP 10: AERODYNAMIC COEFFICIENTS
        # Unit span is used because span was not supplied.
        # ------------------------------------------------------

        reference_area_per_span = chord * 1.0

        CL = (
            lift_per_span /
            (q_inf * reference_area_per_span)
        )

        CD = (
            drag_per_span /
            (q_inf * reference_area_per_span)
        )

        print("\n========== STEP 10: AERODYNAMIC COEFFICIENTS ==========")

        print("\nReference area per unit span:")
        print("S' = chord * 1")
        print(f"S' = {reference_area_per_span:.8f} m^2/m")

        print("\nLift coefficient:")
        print("CL = L' / (q_inf * chord)")
        print(
            f"CL = {lift_per_span:.8f} / "
            f"({q_inf:.8f} * {chord:.8f})"
        )
        print(f"CL = {CL:.8f}")

        print("\nDrag coefficient:")
        print("CD = D' / (q_inf * chord)")
        print(
            f"CD = {drag_per_span:.8f} / "
            f"({q_inf:.8f} * {chord:.8f})"
        )
        print(f"CD = {CD:.8f}")

        print("\nLift-to-drag ratio:")
        if abs(drag_per_span) > 1e-12:
            print("L/D = L' / D'")
            print(
                f"L/D = {lift_per_span:.8f} / "
                f"{drag_per_span:.8f}"
            )
            print(
                f"L/D = {lift_per_span / drag_per_span:.8f}"
            )
        else:
            print("L/D is undefined because drag is zero.")

        # ------------------------------------------------------
        # STEP 11: FINAL SUMMARY
        # ------------------------------------------------------

        print("\n================================================")
        print("             FINAL DIAMOND AIRFOIL RESULTS")
        print("================================================")

        print(f"Chord                  = {chord:.8f} m")
        print(f"Maximum thickness      = {thickness:.8f} m")
        print(f"Mach number             = {M_inf:.8f}")
        print(f"Freestream pressure     = {p_inf:.8f} Pa")
        print(f"Half-angle epsilon      = {epsilon_deg:.8f} deg")
        print(f"Angle of attack         = {alpha_deg:.8f} deg")

        print(f"Upper-front pressure    = {p_upper_front:.8f} Pa")
        print(f"Upper-rear pressure     = {p_upper_rear:.8f} Pa")
        print(f"Lower-front pressure    = {p_lower_front:.8f} Pa")
        print(f"Lower-rear pressure     = {p_lower_rear:.8f} Pa")

        print(f"Lift per span L'        = {lift_per_span:.8f} N/m")
        print(f"Drag per span D'        = {drag_per_span:.8f} N/m")
        print(f"Lift coefficient CL    = {CL:.8f}")
        print(f"Drag coefficient CD    = {CD:.8f}")

        print("\nTotal L and D:")
        print("Not calculated: span was not one of the five inputs.")
        print("For a known span b: L = L' * b and D = D' * b.")

        print("\nAbsolute T, rho, V and a:")
        print("Not determined from Mach number and pressure alone.")
        print("The pressure ratios and aerodynamic coefficients above")
        print("do not require those additional freestream properties.")


    # ==========================================================
    # MAIN CHAPTER 9 LOOP
    # ==========================================================

    while True:
        print("\n======================================================")
        print("      CHAPTER 9 - BASIC COMPRESSIBLE FLOW")
        print("======================================================")

        print("[1] Sequential shocks and expansion fans")
        print("[2] Opposing shock interaction - Figure 9.21")
        print("[3] Same-direction wave interaction - Figure 9.22")
        print("[4] Flat-plate airfoil: shock, expansion, L, D, CL, CD")
        print("[5] Diamond airfoil: shock, expansion, L, D, CL, CD")
        print("[0] Return to main menu")

        choice = input("Select option: ").strip()

        if choice == "0":
            return

        if choice not in ("1", "2", "3" , "4" , "5"):
            print("Invalid selection.")
            continue

        print("\n========== GAS PROPERTIES ==========")

        gamma = ask_float(
            "Specific heat ratio gamma [1.4]: ",
            default=1.4,
            minimum=1.0
        )

        R = ask_float(
            "Specific gas constant R [287]: ",
            default=287.0,
            minimum=0.0
        )

        region1 = initial_region()

        if region1 is None:
            continue

        # Interaction calculations use the same freestream.
        if choice == "2":
            opposing_interaction(region1)
            continue

        if choice == "3":
            same_direction_interaction(region1)
            continue
        elif choice == "4":
            flat_plate_airfoil()

            if not ask_yes_no("\nSolve another Chapter 9 problem?"):
                return

            continue
        elif choice == "5":
            diamond_airfoil()

            if not ask_yes_no("\nSolve another Chapter 9 problem?"):
                return

            continue

        # Choice 1 continues into your original sequential solver.


        regions = [region1]
        layer_results = []

        number_of_layers = int(
            ask_float(
                "Number of shock/expansion layers: ",
                minimum=0.0
            )
        )

        if number_of_layers < 1:
            print("At least one layer is required.")
            continue

        successful_layers = 0

        for layer in range(1, number_of_layers + 1):
            print(
                f"\n\n================ LAYER {layer} "
                f"OF {number_of_layers} ================"
            )

            print("[1] Oblique shock")
            print("[2] Normal shock")
            print("[3] Expansion fan")
            print("[0] Stop sequence")

            layer_type = ask_choice(
                "Select layer type: ",
                ["1", "2", "3", "0"]
            )

            if layer_type == "0":
                print("Sequence stopped by user.")
                break

            upstream = regions[-1]

            if layer_type == "1":
                downstream, result = apply_oblique_shock(
                    upstream, layer
                )

            elif layer_type == "2":
                downstream, result = apply_normal_shock(
                    upstream, layer
                )

            else:
                downstream, result = apply_expansion(
                    upstream, layer
                )

            if downstream is None:
                print(
                    f"Layer {layer} could not be calculated. "
                    "Sequence stopped."
                )
                break

            result["layer"] = layer
            layer_results.append(result)

            downstream = collect_region_properties(
                len(regions) + 1,
                downstream
            )

            regions.append(downstream)
            successful_layers += 1

        print("\n\n======================================================")
        print("                    FINAL RESULTS")
        print("======================================================")

        display_layer_table(layer_results)
        display_regions(regions)

        print(f"\nSuccessfully calculated layers: {successful_layers}")
        print(f"Total calculated regions: {len(regions)}")

        print("\nNotes:")
        print("- N/A means that a property could not be determined.")
        print("- Angles are displayed in degrees.")
        print("- Pressure is in Pa; temperature is in K.")
        print("- Density is in kg/m3; velocity is in m/s.")
        print("- Normal shock: theta = 0 degrees, beta = 90 degrees.")
        print("- Expansion fans do not have a shock angle beta.")
        print("- Mn1 and Mn2 are not applicable to expansion fans.")

        if not ask_yes_no("\nSolve another Chapter 9 problem?"):
            return



# ==========================================================
# 11. MAIN MENU
# ==========================================================

def main():

    while True:

        print("\n========================================")
        print("       ANDERSON AERODYNAMICS TOOLBOX")
        print("========================================")

        print("[1] Chapter 7")
        print("[2] Chapter 8")
        print("[3] Chapter 9")
        print("[0] Exit")

        choice = input("\nSelect chapter: ")

        if choice == "1":
            chapter_7()

        elif choice == "2":
            chapter_8()
        elif choice == "3":
            chapter9()

        elif choice == "0":
            print("Program terminated.")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
