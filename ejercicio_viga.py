import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="WIPACE - Viga Hiperestática 4", layout="wide"
)

st.title("Web Interactiva para el Cálculo de Estructuras (WIPACE)")
st.subheader("Ejercicio: Viga Hiperestática de 3 Vanos con Voladizo")

# ---------------------------------------------------------
# 1. BARRA LATERAL: PARÁMETROS DE ENTRADA
# ---------------------------------------------------------
st.sidebar.header("1. Geometría y Longitudes (m)")
L1 = st.sidebar.number_input("L1 (m)", min_value=0.1, value=2.0, step=0.5)
L2 = st.sidebar.number_input("L2 (m)", min_value=0.1, value=3.0, step=0.5)
L3 = st.sidebar.number_input("L3 (m)", min_value=0.1, value=2.5, step=0.5)
L4 = st.sidebar.number_input("L4 (m)", min_value=0.1, value=2.5, step=0.5)
L5 = st.sidebar.number_input("L5 (m)", min_value=0.1, value=2.0, step=0.5)

st.sidebar.header("2. Cargas Aplicadas")
P1 = st.sidebar.number_input("P1 (kN)", value=10.0, step=1.0)
H1 = st.sidebar.number_input("H1 (kN)", value=5.0, step=1.0)
H2 = st.sidebar.number_input("H2 (kN)", value=3.0, step=1.0)
M1 = st.sidebar.number_input("M1 (kN·m)", value=4.0, step=1.0)
M2 = st.sidebar.number_input("M2 (kN·m)", value=6.0, step=1.0)
M3 = st.sidebar.number_input("M3 (kN·m)", value=5.0, step=1.0)
q1 = st.sidebar.number_input("q1 (kN/m)", value=8.0, step=1.0)

L_total = L1 + L2 + L3 + L4 + L5


# ---------------------------------------------------------
# 2. ESQUEMA GEOMÉTRICO SUPERIOR
# ---------------------------------------------------------
def dibujar_esquema():
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.plot([0, L_total], [0, 0], "k-", lw=3)  # Eje de la viga

    # Puntos característicos
    xB = L1 + L2
    xC = L1 + L2 + L3 + L4
    xD = L_total

    # Nodos
    ax.text(0, -0.4, "A", fontsize=12, weight="bold", ha="center")
    ax.text(xB, -0.4, "B", fontsize=12, weight="bold", ha="center")
    ax.text(xC, -0.4, "C", fontsize=12, weight="bold", ha="center")
    ax.text(xD, -0.4, "D", fontsize=12, weight="bold", ha="center")

    # Apoyo A (Empotramiento)
    ax.plot([0, 0], [-0.3, 0.3], "k-", lw=4)
    for y_hatch in np.linspace(-0.3, 0.3, 7):
        ax.plot([0, -0.15], [y_hatch, y_hatch - 0.08], "k-", lw=1)

    # Apoyos móviles en B y C (Triángulos)
    ax.plot(
        [xB, xB - 0.2, xB + 0.2, xB], [0, -0.25, -0.25, 0], "k-", lw=1.5
    )
    ax.plot(
        [xC, xC - 0.2, xC + 0.2, xC], [0, -0.25, -0.25, 0], "k-", lw=1.5
    )

    # Representación de Fuerzas
    if P1 != 0:
        ax.annotate(
            f"P1={P1}",
            xy=(L1, 0),
            xytext=(L1, -0.7),
            arrowprops=dict(facecolor="red", shrink=0.05, width=1.5),
            ha="center",
            color="red",
        )
    if H1 != 0:
        ax.annotate(
            f"H1={H1}",
            xy=(L1, 0.1),
            xytext=(L1 + 0.6, 0.1),
            arrowprops=dict(facecolor="blue", shrink=0.05, width=1.5),
            ha="center",
            color="blue",
        )
    if H2 != 0:
        ax.annotate(
            f"H2={H2}",
            xy=(xD, 0.1),
            xytext=(xD + 0.6, 0.1),
            arrowprops=dict(facecolor="blue", shrink=0.05, width=1.5),
            ha="center",
            color="blue",
        )
    if q1 != 0:
        x_q = np.linspace(xC, xD, 8)
        for xq in x_q:
            ax.annotate(
                "",
                xy=(xq, 0),
                xytext=(xq, 0.4),
                arrowprops=dict(arrowstyle="->", color="purple", lw=1),
            )
        ax.plot([xC, xD], [0.4, 0.4], "purple", lw=1.5)
        ax.text(
            (xC + xD) / 2, 0.5, f"q1={q1} kN/m", color="purple", ha="center"
        )

    # Cotas de longitudes
    y_cota = -0.9
    cotas = [0, L1, L1 + L2, L1 + L2 + L3, L1 + L2 + L3 + L4, L_total]
    etiquetas = ["L1", "L2", "L3", "L4", "L5"]
    for i in range(len(etiquetas)):
        ax.plot([cotas[i], cotas[i + 1]], [y_cota, y_cota], "k|-", lw=1)
        ax.text(
            (cotas[i] + cotas[i + 1]) / 2,
            y_cota - 0.15,
            etiquetas[i],
            ha="center",
            fontsize=9,
        )

    ax.set_xlim(-0.5, L_total + 1)
    ax.set_ylim(-1.3, 0.8)
    ax.axis("off")
    st.pyplot(fig)


st.markdown("### Esquema Geométrico de la Viga")
dibujar_esquema()

# ---------------------------------------------------------
# 3. MOTOR DE CÁLCULO ESTRUCTURAL (Fórmulas PDF)
# ---------------------------------------------------------
# El botón de calcular procesa los diagramas
calcular = st.button(
    "Calcular Diagramas de Esfuerzos", type="primary", use_container_width=True
)

if calcular or "calculado" in st.session_state:
    st.session_state["calculado"] = True

    # Incógnitas hiperestáticas A1 y A2 (PDF página 2)
    num_A1 = (
        3 * M1 * (L1 + L2)
        + (3 * (-P1) * (L1**2) * L2) / (L1 + L2)
        + 2 * (L3 + L4) * (q1 * (L5**2) / 2 + M3)
        + 2 * (-M2) * (2 * (L4**2) - (L3**2) - 2 * L3 * L4) / (L3 + L4)
    )
    den_A1 = 3 * L1 + 3 * L2 + 4 * L3 + 4 * L4
    A1 = -num_A1 / den_A1
    A2 = -0.5 * (
        A1 + M1 + ((-P1) * L1 * L2 * (L1 + 2 * L2)) / ((L1 + L2) ** 2)
    )

    x = np.linspace(0, L_total, 1000)
    N = np.zeros_like(x)
    V = np.zeros_like(x)
    M = np.zeros_like(x)

    # Evaluación por tramos según las ecuaciones del PDF
    for i, xi in enumerate(x):
        # Axiles N(x)
        if xi < L1:
            N[i] = H1 + H2
        else:
            N[i] = H2

        # Cortantes V(x) y Momentos M(x)
        if xi < L1:
            V[i] = A2 / (L1 + L2) - (-P1 * L2) / (L1 + L2) - (M1 + A1) / (L1 + L2)
            M[i] = (
                -A2 * (1 - xi / (L1 + L2))
                - (M1 + A1) * (xi / (L1 + L2))
                - xi * (-P1 * L2) / (L1 + L2)
            )
        elif xi < L1 + L2:
            V[i] = A2 / (L1 + L2) + (-P1 * L1) / (L1 + L2) - (M1 + A1) / (L1 + L2)
            M[i] = (
                -A2 * (1 - xi / (L1 + L2))
                - (M1 + A1) * (xi / (L1 + L2))
                - (L1 + L2 - xi) * (-P1 * L1) / (L1 + L2)
            )
        elif xi < L1 + L2 + L3:
            V[i] = (
                A1 / (L3 + L4)
                + (-M2) / (L3 + L4)
                - (q1 * (L5**2) / 2 + M3) / (L3 + L4)
            )
            M[i] = (
                -A1 * (1 - (xi - L1 - L2) / (L3 + L4))
                - (q1 * (L5**2) / 2 + M3) * (xi - L1 - L2) / (L3 + L4)
                - M2 * (xi - L1 - L2) / (L3 + L4)
            )
        elif xi < L1 + L2 + L3 + L4:
            V[i] = (
                A1 / (L3 + L4)
                + (-M2) / (L3 + L4)
                - (q1 * (L5**2) / 2 + M3) / (L3 + L4)
            )
            M[i] = (
                -A1 * (1 - (xi - L1 - L2) / (L3 + L4))
                - (q1 * (L5**2) / 2 - M3) * (xi - L1 - L2) / (L3 + L4)
                + M2 * (L1 + L2 + L3 + L4 - xi) / (L3 + L4)
            )
        else:
            V[i] = q1 * (L_total - xi)
            M[i] = -q1 * ((L_total - xi) ** 2) / 2 + M3

    # ---------------------------------------------------------
    # 4. REPRESENTACIÓN DE DIAGRAMAS DE ESFUERZOS (N, V, M)
    # ---------------------------------------------------------
    st.markdown("### Diagramas de Leyes de Esfuerzos")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Incógnita Hiperestática A1", f"{A1:.3f} kN·m")
    with col2:
        st.metric("Incógnita Hiperestática A2", f"{A2:.3f} kN·m")

    fig_diag, (ax_N, ax_V, ax_M) = plt.subplots(3, 1, figsize=(10, 7), sharex=True)

    # Esfuerzo Axil N(x)
    ax_N.plot(x, N, "b-", lw=1.5)
    ax_N.fill_between(x, N, color="blue", alpha=0.15)
    ax_N.set_ylabel("Axil N (kN)")
    ax_N.grid(True, linestyle="--", alpha=0.5)
    ax_N.set_title("Ley de Esfuerzos Axiles")

    # Esfuerzo Cortante V(x)
    ax_V.plot(x, V, "r-", lw=1.5)
    ax_V.fill_between(x, V, color="red", alpha=0.15)
    ax_V.set_ylabel("Cortante V (kN)")
    ax_V.grid(True, linestyle="--", alpha=0.5)
    ax_V.set_title("Ley de Esfuerzos Cortantes")

    # Momento Flector M(x) (representado invertido según convenio de estructuras)
    ax_M.plot(x, M, "g-", lw=1.5)
    ax_M.fill_between(x, M, color="green", alpha=0.15)
    ax_M.set_ylabel("Flector M (kN·m)")
    ax_M.set_xlabel("Posición x (m)")
    ax_M.grid(True, linestyle="--", alpha=0.5)
    ax_M.set_title("Ley de Momentos Flectores")
    ax_M.invert_yaxis()  # Convenio habitual: flectores positivos hacia abajo

    plt.tight_layout()
    st.pyplot(fig_diag)

    # ---------------------------------------------------------
    # 5. SECCIÓN DE LA DEFORMADA (Modificación de E e I)
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### Cálculo de la Deformada de la Viga")
    st.write(
        "Ajusta las propiedades del material y de la sección transversal para visualizar la flecha/deformada:"
    )

    col_E, col_I = st.columns(2)
    with col_E:
        E_val = st.number_input(
            "Módulo Elástico E (kN/m²)",
            value=2.1e8,
            format="%.2e",
            help="Ejemplo: Acero ≈ 2.1e8 kN/m² (210 GPa)",
        )
    with col_I:
        I_val = st.number_input(
            "Momento de Inercia I (m⁴)",
            value=8.33e-5,
            format="%.2e",
            help="Ejemplo: Perfil IPE 300 ≈ 8.33e-5 m⁴",
        )

    if E_val > 0 and I_val > 0:
        # Integración numérica doble para la deformada v(x)
        dx = x[1] - x[0]
        theta = np.cumsum(M / (E_val * I_val)) * dx
        v = np.cumsum(theta) * dx  # Deflexión vertical v(x) en metros

        fig_def, ax_def = plt.subplots(figsize=(10, 3))
        ax_def.plot([0, L_total], [0, 0], "k--", alpha=0.5, label="Eje neutro sin deformar")
        ax_def.plot(
            x, v * 1000, "m-", lw=2, label="Deformada v(x)"
        )  # Convertido a mm
        ax_def.set_ylabel("Flecha v (mm)")
        ax_def.set_xlabel("Posición x (m)")
        ax_def.set_title("Deformada de la Viga v(x)")
        ax_def.grid(True, linestyle="--", alpha=0.5)
        ax_def.invert_yaxis()  # Deflexión hacia abajo positiva visualmente
        ax_def.legend(loc="upper right")

        # Marcar apoyos
        ax_def.plot([0, L1 + L2, L1 + L2 + L3 + L4], [0, 0, 0], "ko", ms=6)

        plt.tight_layout()
        st.pyplot(fig_def)

        max_v = np.max(np.abs(v)) * 1000
        st.info(f"**Flecha máxima calculada:** {max_v:.3f} mm")
