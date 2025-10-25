import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Annotation

import math

#funcion AngleAnnotation de la página de ejemplos
import numpy as np

from matplotlib.patches import Arc
from matplotlib.transforms import Bbox, IdentityTransform, TransformedBbox

class AngleAnnotation(Arc):
    """
    Draws an arc between two vectors which appears circular in display space.
    """
    def __init__(self, xy, p1, p2, size=75, unit="points", ax=None,
                 text="", textposition="inside", text_kw=None, **kwargs):
        """
        Parameters
        ----------
        xy, p1, p2 : tuple or array of two floats
            Center position and two points. Angle annotation is drawn between
            the two vectors connecting *p1* and *p2* with *xy*, respectively.
            Units are data coordinates.

        size : float
            Diameter of the angle annotation in units specified by *unit*.

        unit : str
            One of the following strings to specify the unit of *size*:

            * "pixels": pixels
            * "points": points, use points instead of pixels to not have a
              dependence on the DPI
            * "axes width", "axes height": relative units of Axes width, height
            * "axes min", "axes max": minimum or maximum of relative Axes
              width, height

        ax : `matplotlib.axes.Axes`
            The Axes to add the angle annotation to.

        text : str
            The text to mark the angle with.

        textposition : {"inside", "outside", "edge"}
            Whether to show the text in- or outside the arc. "edge" can be used
            for custom positions anchored at the arc"s edge.

        text_kw : dict
            Dictionary of arguments passed to the Annotation.

        **kwargs
            Further parameters are passed to `matplotlib.patches.Arc`. Use this
            to specify, color, linewidth etc. of the arc.

        """
        self.ax = ax or plt.gca()
        self._xydata = xy  # in data coordinates
        self.vec1 = p1
        self.vec2 = p2
        self.size = size
        self.unit = unit
        self.textposition = textposition

        super().__init__(self._xydata, size, size, angle=0.0,
                         theta1=self.theta1, theta2=self.theta2, **kwargs)

        self.set_transform(IdentityTransform())
        self.ax.add_patch(self)

        self.kw = dict(ha="center", va="center",
                       xycoords=IdentityTransform(),
                       xytext=(0, 0), textcoords="offset points",
                       annotation_clip=True)
        self.kw.update(text_kw or {})
        self.text = ax.annotate(text, xy=self._center, **self.kw)

    def get_size(self):
        factor = 1.
        if self.unit == "points":
            factor = self.ax.figure.dpi / 72.
        elif self.unit[:4] == "axes":
            b = TransformedBbox(Bbox.unit(), self.ax.transAxes)
            dic = {"max": max(b.width, b.height),
                   "min": min(b.width, b.height),
                   "width": b.width, "height": b.height}
            factor = dic[self.unit[5:]]
        return self.size * factor

    def set_size(self, size):
        self.size = size

    def get_center_in_pixels(self):
        """return center in pixels"""
        return self.ax.transData.transform(self._xydata)

    def set_center(self, xy):
        """set center in data coordinates"""
        self._xydata = xy

    def get_theta(self, vec):
        vec_in_pixels = self.ax.transData.transform(vec) - self._center
        return np.rad2deg(np.arctan2(vec_in_pixels[1], vec_in_pixels[0]))

    def get_theta1(self):
        return self.get_theta(self.vec1)

    def get_theta2(self):
        return self.get_theta(self.vec2)

    def set_theta(self, angle):
        pass

    # Redefine attributes of the Arc to always give values in pixel space
    _center = property(get_center_in_pixels, set_center)
    theta1 = property(get_theta1, set_theta)
    theta2 = property(get_theta2, set_theta)
    width = property(get_size, set_size)
    height = property(get_size, set_size)

    # The following two methods are needed to update the text position.
    def draw(self, renderer):
        self.update_text()
        super().draw(renderer)

    def update_text(self):
        c = self._center
        s = self.get_size()
        angle_span = (self.theta2 - self.theta1) % 360
        angle = np.deg2rad(self.theta1 + angle_span / 2)
        r = s / 2
        if self.textposition == "inside":
            r = s / np.interp(angle_span, [60, 90, 135, 180],
                                          [3.3, 3.5, 3.8, 4])
        self.text.xy = c + r * np.array([np.cos(angle), np.sin(angle)])
        if self.textposition == "outside":
            def R90(a, r, w, h):
                if a < np.arctan(h/2/(r+w/2)):
                    return np.sqrt((r+w/2)**2 + (np.tan(a)*(r+w/2))**2)
                else:
                    c = np.sqrt((w/2)**2+(h/2)**2)
                    T = np.arcsin(c * np.cos(np.pi/2 - a + np.arcsin(h/2/c))/r)
                    xy = r * np.array([np.cos(a + T), np.sin(a + T)])
                    xy += np.array([w/2, h/2])
                    return np.sqrt(np.sum(xy**2))

            def R(a, r, w, h):
                aa = (a % (np.pi/4))*((a % (np.pi/2)) <= np.pi/4) + \
                     (np.pi/4 - (a % (np.pi/4)))*((a % (np.pi/2)) >= np.pi/4)
                return R90(aa, r, *[w, h][::int(np.sign(np.cos(2*a)))])

            bbox = self.text.get_window_extent()
            X = R(angle, r, bbox.width, bbox.height)
            trans = self.ax.figure.dpi_scale_trans.inverted()
            offs = trans.transform(((X-s/2), 0))[0] * 72
            self.text.set_position([offs*np.cos(angle), offs*np.sin(angle)])

# un proyectil es lanzado a una velocidad inicial vi, con un angulo de angv,
# recorre una distancia d, a lo largo de un tiempo dt.

def trianguloDesplazamiento(vi, angv, tf, 
                            mostrarAngulo=False, 
                            mostrarDesplazamientoX=False, 
                            mostrarDesplazamientoY=False,
                            mostrarDesplazamiento=False):
    # vi    : velocidad inicial en [m/s]
    # angv  : angulo del vector velocidad inicial en deg
    fig, ax = plt.subplots()

    vix = vi * math.cos(math.radians(angv))
    viy = vi * math.sin(math.radians(angv))

    grav = 10   # gravedad redondeada
    dt = tf      # delta tiempo


    velocidad = FancyArrowPatch((0, 0), 
                                (vix*dt, viy*dt), 
                                color="xkcd:cobalt blue", 
                                mutation_scale=20)
    ax.annotate(r"$\vec{v}_0 \Delta t$", 
                xy=(vix*dt/2, viy*dt/2),
                xytext=(-25,7),
                textcoords="offset points",
                fontsize=12)
    
    aceleracion = FancyArrowPatch((vix*dt,viy*dt),
                                (vix*dt, viy * dt - grav * dt**2),
                                color="xkcd:scarlet",
                                mutation_scale=20)
    ax.annotate(r"$\vec{g} \Delta t^2$",
                xy=(vix*dt, (viy * dt - (grav / 2) * dt**2)),
                xytext=(7,0),
                textcoords="offset points",
            fontsize=12)

    desplazamiento = FancyArrowPatch((0, 0),
                                     (vix*dt, viy * dt - grav*dt**2),
                                     color="xkcd:steel grey",
                                     mutation_scale=20)
    ax.annotate(r"$\vec{D}$",
                (vix*dt/2,(viy * dt - grav*dt**2)/2),
                xytext=(-25,-15), 
                textcoords="offset points",
                fontsize=12)



    ax.hlines(0,0,vix * dt, ls="--")
    ax.add_patch(velocidad)
    ax.add_patch(aceleracion)
    ax.add_patch(desplazamiento)

    ax.set_aspect("equal")
    ax.spines[["top", "right"]].set_visible(False)
    


    ax.set(xlim=(0,vix*dt * 1.05),
           ylim=(viy*dt -grav*dt**2 * 1.05,viy*dt * 1.05))
           
    ax.spines.bottom.set_position(("axes", 0))

    # Agregando informacion para estudiante

    if mostrarAngulo:
        AngleAnnotation((0,0), 
                        (vix*dt,0), 
                        (vix*dt,viy*dt),
                        size=100*vix*dt*0.05, 
                        ax=ax, text=str(angv)+"°", 
                        textposition="inside", 
                        unit="pixels")

    if mostrarDesplazamientoX: ax.set_xticks([vix*dt])
    else: ax.set_xticks([])
    if mostrarDesplazamientoY: ax.set_yticks([viy*dt -grav*dt**2, 0, viy*dt])
    else: ax.set_yticks([])

    ###

    fig.set_figheight(7)
    fig.savefig("test.png")

    plt.show()

trianguloDesplazamiento(25, 30, 3, True, True, True, True)
