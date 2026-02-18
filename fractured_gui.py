#!/usr/bin/env python3
"""
Fractured Key - Premium Modern GUI
A next-generation secure authentication system with a 2025 SaaS-style interface.
Blue theme with glassmorphism, smooth animations, and premium typography.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, Canvas
import threading
import os
import sys
import subprocess
import platform
import shutil
from PIL import Image, ImageDraw, ImageFilter
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from steganography import embed_data_into_image, extract_data_from_image
from sss import split_bytes_into_shares, recover_bytes_from_shares
from crypto import encrypt_password_aes_gcm, decrypt_password_aes_gcm

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR SCHEME - Attractive light blue (sky / cyan) theme
# Futuristic, secure, premium SaaS 2025
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    # Primary backgrounds (dark base for contrast)
    BG_DARKEST = "#050B14"
    BG_DARK = "#0A1628"
    BG_MEDIUM = "#0F172A"
    BG_LIGHT = "#1E293B"
    BG_HOVER = "#334155"

    # Light blue accents (attractive sky / cyan)
    BLUE_DEEP = "#0C4A6E"        # Dark teal-blue (top bar, depth)
    BLUE_NEON = "#38BDF8"        # Light sky blue (primary accent)
    BLUE_SKY = "#22D3EE"         # Cyan
    BLUE_LIGHT = "#7DD3FC"       # Light sky
    BLUE_GLOW = "#BAE6FD"        # Soft glow / hover

    # Primary accent — attractive light blue
    ACCENT_PRIMARY = "#38BDF8"   # Light sky blue
    ACCENT_GLOW = "#7DD3FC"      # Lighter on hover
    ACCENT_MUTED = "#0EA5E9"     # Sky blue
    ACCENT_DARK = "#0284C7"      # Deeper for contrast

    # Semantic colors
    SUCCESS = "#10B981"
    SUCCESS_GLOW = "#059669"
    WARNING = "#F59E0B"
    ERROR = "#EF4444"
    ERROR_GLOW = "#DC2626"

    # Text colors
    TEXT_PRIMARY = "#F8FAFC"
    TEXT_SECONDARY = "#94A3B8"
    TEXT_MUTED = "#64748B"
    TEXT_ACCENT = "#7DD3FC"

    # Border and dividers - adjusted for pixelated aesthetic
    BORDER = "#475569"  # Lighter gray for better visibility
    BORDER_GLOW = "#38BDF840"
    BORDER_LIGHT = "#64748B"  # Even lighter gray like in the image
    
    # Icon symbols - Unicode/Emoji that work across platforms
    ICON_LOCK = "🔒"
    ICON_UNLOCK = "🔓"
    ICON_FOLDER = "📁"
    ICON_INFO = "ℹ️"
    ICON_KEY = "🔑"
    ICON_IMAGE = "🖼️"
    ICON_TRASH = "🗑️"
    ICON_SETTINGS = "⚙️"
    ICON_SECURITY = "🛡️"
    ICON_CHECK = "✓"
    ICON_CROSS = "✗"
    ICON_WARNING = "⚠️"
    ICON_ROCKET = "🚀"
    ICON_SPARKLES = "✨"
    ICON_LIGHTNING = "⚡"

# ═══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY - Modern attractive fonts
# ═══════════════════════════════════════════════════════════════════════════════

# Try modern fonts in order of preference - system will use first available
# Inter, Poppins, and Roboto are modern, clean fonts
# Fallback to system defaults if not available
import tkinter.font as tkfont

def get_available_font():
    """Get the first available attractive font"""
    preferred_fonts = ["Inter", "Poppins", "Roboto", "Segoe UI", "system-ui"]
    
    # Get all available fonts
    try:
        available_fonts = list(tkfont.families())
        for font in preferred_fonts:
            if font in available_fonts:
                return font
    except:
        pass
    
    # Fallback to system default
    return "Segoe UI"

_FONT_FAMILY = get_available_font()

def get_available_emoji_font():
    """Pick an emoji-capable font (Linux friendly)."""
    preferred = ["Noto Color Emoji", "Segoe UI Emoji", "Apple Color Emoji", "Twitter Color Emoji"]
    try:
        available = set(tkfont.families())
        for f in preferred:
            if f in available:
                return f
    except Exception:
        pass
    return _FONT_FAMILY

_EMOJI_FONT = get_available_emoji_font()

class Fonts:
    FAMILY = _FONT_FAMILY
    FAMILY_MONO = "Cascadia Code"

    # Slightly larger typography for better Linux readability
    HERO = (FAMILY, 50, "bold")
    HERO_SM = (FAMILY, 38, "bold")
    TITLE_XL = (FAMILY, 30, "bold")
    TITLE_LG = (FAMILY, 23, "bold")
    TITLE_MD = (FAMILY, 19, "bold")
    TITLE_SM = (FAMILY, 15, "bold")

    BODY_LG = (FAMILY, 15)
    BODY_MD = (FAMILY, 13)
    BODY_SM = (FAMILY, 12)

    MONO_LG = ("Cascadia Code", 12)
    MONO_MD = ("Cascadia Code", 11)
    MONO_SM = ("Cascadia Code", 10)

    BUTTON = (FAMILY, 14, "bold")
    LABEL = (FAMILY, 13, "bold")
    CAPTION = (FAMILY, 11)
    TAGLINE = (FAMILY, 17)

    EMOJI_LG = (_EMOJI_FONT, 30)
    EMOJI_MD = (_EMOJI_FONT, 22)
    EMOJI_SM = (_EMOJI_FONT, 20)

# ═══════════════════════════════════════════════════════════════════════════════
# FILE DIALOG HELPERS - Native Linux file manager integration
# ═══════════════════════════════════════════════════════════════════════════════

def native_file_dialog(parent_window, title, filetypes, mode="open", initialdir=None, defaultextension=""):
    """
    Open native file dialog that integrates with Linux file managers.
    Uses tkinter's filedialog but with better Linux integration.
    """
    if initialdir is None:
        initialdir = os.path.expanduser("~")

    # On Linux, prefer the desktop portal/zenity/kdialog dialog (better touchpad + WM integration)
    # Falls back to tkinter dialogs if helpers are not available.
    if platform.system() == "Linux":
        # GNOME / common
        if shutil.which("zenity"):
            try:
                cmd = ["zenity", "--file-selection", "--title", title]
                if mode == "save":
                    cmd += ["--save", "--confirm-overwrite"]
                if initialdir:
                    # zenity expects a trailing slash for directory
                    cmd += ["--filename", os.path.join(initialdir, "")]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0:
                    path = res.stdout.strip()
                    if mode == "save" and defaultextension and path and not os.path.splitext(path)[1]:
                        path += defaultextension
                    return path
                return ""
            except Exception:
                pass

        # KDE
        if shutil.which("kdialog"):
            try:
                if mode == "save":
                    cmd = ["kdialog", "--getsavefilename", os.path.join(initialdir, ""), "*"]
                else:
                    cmd = ["kdialog", "--getopenfilename", os.path.join(initialdir, ""), "*"]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0:
                    path = res.stdout.strip()
                    if mode == "save" and defaultextension and path and not os.path.splitext(path)[1]:
                        path += defaultextension
                    return path
                return ""
            except Exception:
                pass
    
    # Ensure parent window is raised and focused
    try:
        parent_window.lift()
        parent_window.focus_force()
        parent_window.update_idletasks()
    except:
        pass
    
    if mode == "save":
        file_path = filedialog.asksaveasfilename(
            parent=parent_window,
            title=title,
            filetypes=filetypes,
            initialdir=initialdir,
            defaultextension=defaultextension
        )
    else:
        file_path = filedialog.askopenfilename(
            parent=parent_window,
            title=title,
            filetypes=filetypes,
            initialdir=initialdir
        )
    
    return file_path

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM WIDGETS - Glassmorphism, neumorphism, micro-interactions
# ═══════════════════════════════════════════════════════════════════════════════

_SMOOTH_SCROLL_JOBS = {}

def smooth_scroll(canvas, delta_units, *, steps=12, delay_ms=8):
    """
    Smooth scrolling animation that works well with Linux touchpads.
    Cancels any in-flight animation for the same canvas to keep the scroll bar and touchpad in sync.
    """
    if not canvas:
        return

    # Cancel any previous smooth scroll for this canvas
    key = str(canvas)
    job = _SMOOTH_SCROLL_JOBS.get(key)
    if job is not None:
        try:
            canvas.after_cancel(job)
        except Exception:
            pass
        _SMOOTH_SCROLL_JOBS.pop(key, None)

    # Use an accumulator so small deltas still move (no int(0) problem)
    total = float(delta_units)
    per_step = total / float(max(1, steps))
    acc = 0.0
    step = 0

    def _tick():
        nonlocal acc, step
        if step >= steps:
            _SMOOTH_SCROLL_JOBS.pop(key, None)
            return
        step += 1

        acc += per_step
        move = int(acc)
        acc -= move

        try:
            if move != 0:
                canvas.yview_scroll(move, "units")
        except Exception:
            _SMOOTH_SCROLL_JOBS.pop(key, None)
            return

        _SMOOTH_SCROLL_JOBS[key] = canvas.after(delay_ms, _tick)

    _tick()

def enable_touchpad_scrolling(scrollable_frame):
    """
    Kept for backward compatibility.
    Scrolling is handled globally (under-cursor routing) inside the app via `_setup_global_scrolling()`.
    """
    return

class PixelatedCard(ctk.CTkFrame):
    """Card with pixelated/notched border style - Linux retro aesthetic"""
    def __init__(self, master, **kwargs):
        # Remove corner_radius to create sharp corners for pixelated effect
        kwargs.pop('corner_radius', None)
        border_width = kwargs.pop('border_width', 2)
        border_color = kwargs.pop('border_color', Colors.BORDER_LIGHT)
        
        super().__init__(
            master,
            fg_color=Colors.BG_MEDIUM,
            corner_radius=0,  # Sharp corners for pixelated look
            border_width=border_width,
            border_color=border_color,
            **kwargs
        )
        
        # Store border properties
        self._notch_size = 8  # Size of the L-shaped notch at corners
        self._border_color = border_color
        self._hover_color = Colors.BLUE_NEON
        self._is_hovered = False
        
        # Create a wrapper frame with canvas overlay for custom border
        self._border_overlay = None
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._on_configure)
        
        # Draw border after widget is placed
        self.after_idle(self._draw_border)
    
    def _on_configure(self, event=None):
        """Redraw border when widget is resized"""
        if event and event.widget == self:
            self.after_idle(self._draw_border)
    
    def _draw_border(self):
        """Draw pixelated border with notched corners using canvas overlay"""
        try:
            width = self.winfo_width()
            height = self.winfo_height()
            
            if width <= 1 or height <= 1:
                # Schedule retry
                self.after(50, self._draw_border)
                return
            
            # Remove old border overlay if exists
            if self._border_overlay:
                try:
                    self._border_overlay.destroy()
                except:
                    pass
            
            # Create canvas overlay for custom border
            self._border_overlay = Canvas(
                self,
                highlightthickness=0,
                bg="",  # Transparent
                width=width,
                height=height,
                cursor=""
            )
            self._border_overlay.place(x=0, y=0)
            # Make canvas non-interactive (pass events through)
            self._border_overlay.bind("<Button-1>", lambda e: self.focus_set())
            self._border_overlay.lower()  # Place behind content
            
            notch = self._notch_size
            color = self._hover_color if self._is_hovered else self._border_color
            
            # Draw border with notched corners (pixelated style)
            # Top edge (with gaps for notches)
            self._border_overlay.create_line(notch, 1, width - notch, 1, fill=color, width=2)
            # Right edge
            self._border_overlay.create_line(width - 1, notch, width - 1, height - notch, fill=color, width=2)
            # Bottom edge
            self._border_overlay.create_line(width - notch, height - 1, notch, height - 1, fill=color, width=2)
            # Left edge
            self._border_overlay.create_line(1, height - notch, 1, notch, fill=color, width=2)
            
            # Draw L-shaped notches at corners (creating the pixelated cut-out effect)
            # Top-left corner (L pointing inward/down-right)
            self._border_overlay.create_line(1, notch, notch, notch, fill=color, width=2)
            self._border_overlay.create_line(notch, 1, notch, notch, fill=color, width=2)
            
            # Top-right corner (L pointing inward/down-left)
            self._border_overlay.create_line(width - notch, 1, width - notch, notch, fill=color, width=2)
            self._border_overlay.create_line(width - notch, notch, width - 1, notch, fill=color, width=2)
            
            # Bottom-right corner (L pointing inward/up-left)
            self._border_overlay.create_line(width - notch, height - notch, width - 1, height - notch, fill=color, width=2)
            self._border_overlay.create_line(width - notch, height - notch, width - notch, height - 1, fill=color, width=2)
            
            # Bottom-left corner (L pointing inward/up-right)
            self._border_overlay.create_line(1, height - notch, notch, height - notch, fill=color, width=2)
            self._border_overlay.create_line(notch, height - notch, notch, height - 1, fill=color, width=2)
            
        except Exception as e:
            # Silently fail and retry later
            self.after(100, self._draw_border)
    
    def _on_enter(self, event):
        """Handle hover enter"""
        self._is_hovered = True
        self._draw_border()
    
    def _on_leave(self, event):
        """Handle hover leave"""
        self._is_hovered = False
        self._draw_border()


# Keep GlowingCard as alias for backward compatibility, but use PixelatedCard
GlowingCard = PixelatedCard


class AccentButton(ctk.CTkButton):
    """Primary CTA - pixelated border style"""
    def __init__(self, master, height=52, **kwargs):
        # Use sharp corners for pixelated look
        super().__init__(
            master,
            fg_color=Colors.ACCENT_PRIMARY,
            hover_color=Colors.BLUE_GLOW,
            text_color="#FFFFFF",
            corner_radius=0,  # Sharp corners for pixelated aesthetic
            height=height,
            font=Fonts.BUTTON,
            border_width=2,
            border_color=Colors.ACCENT_PRIMARY,
            **kwargs
        )


class SecondaryButton(ctk.CTkButton):
    """Secondary / outline button - pixelated border"""
    def __init__(self, master, height=48, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            border_width=2,
            border_color=Colors.BORDER_LIGHT,
            corner_radius=0,  # Sharp corners for pixelated aesthetic
            height=height,
            font=Fonts.BODY_MD,
            **kwargs
        )


class SuccessButton(ctk.CTkButton):
    """Success/confirm action button"""
    def __init__(self, master, height=48, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.SUCCESS,
            hover_color=Colors.SUCCESS_GLOW,
            text_color="#FFFFFF",
            corner_radius=14,
            height=height,
            font=Fonts.BUTTON,
            **kwargs
        )


class DangerButton(ctk.CTkButton):
    """Danger/destructive action button"""
    def __init__(self, master, height=48, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.ERROR,
            hover_color=Colors.ERROR_GLOW,
            text_color="#FFFFFF",
            corner_radius=14,
            height=height,
            font=Fonts.BODY_MD,
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    """Styled entry with pixelated border"""
    def __init__(self, master, placeholder="", is_password=False, height=48, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.BG_LIGHT,
            border_color=Colors.BORDER_LIGHT,  # Light gray border like in image
            border_width=2,
            corner_radius=0,  # Sharp corners for pixelated aesthetic
            height=height,
            placeholder_text=placeholder,
            placeholder_text_color=Colors.TEXT_MUTED,
            text_color=Colors.TEXT_PRIMARY,
            font=Fonts.BODY_LG,
            show="●" if is_password else "",
            **kwargs
        )
        self.bind("<FocusIn>", self._on_focus)
        self.bind("<FocusOut>", self._on_unfocus)

    def _on_focus(self, event):
        self.configure(border_color=Colors.ACCENT_PRIMARY)

    def _on_unfocus(self, event):
        self.configure(border_color=Colors.BORDER_LIGHT)


class ModernTextbox(ctk.CTkTextbox):
    """Styled multiline text area"""
    def __init__(self, master, **kwargs):
        corner_radius = kwargs.pop('corner_radius', 14)
        super().__init__(
            master,
            fg_color=Colors.BG_DARKEST,
            border_color=Colors.BORDER,
            border_width=1,
            corner_radius=corner_radius,
            text_color=Colors.TEXT_PRIMARY,
            font=Fonts.MONO_MD,
            scrollbar_button_color=Colors.BG_LIGHT,
            scrollbar_button_hover_color=Colors.BG_HOVER,
            **kwargs
        )


class AnimatedProgress(ctk.CTkProgressBar):
    """Progress bar with blue accent"""
    def __init__(self, master, **kwargs):
        corner_radius = kwargs.pop('corner_radius', 10)
        super().__init__(
            master,
            fg_color=Colors.BG_LIGHT,
            progress_color=Colors.ACCENT_PRIMARY,
            corner_radius=corner_radius,
            height=8,
            **kwargs
        )
        self._animating = False
        self._anim_job = None
        self._phase = 0.0

    def start_animation(self):
        """Start a consistent left→right animation (Linux-friendly)."""
        if self._animating:
            return
        self._animating = True
        # Use determinate mode and animate `set()` ourselves for consistent behavior
        self.configure(mode="determinate")
        self._phase = 0.0

        def tick():
            if not self._animating:
                return
            # Fill left→right then reset (simple, predictable)
            self._phase = (self._phase + 0.02) % 1.0
            try:
                self.set(self._phase)
            except Exception:
                pass
            self._anim_job = self.after(16, tick)  # ~60fps

        tick()

    def stop_animation(self):
        self._animating = False
        if self._anim_job is not None:
            try:
                self.after_cancel(self._anim_job)
            except Exception:
                pass
            self._anim_job = None
        self.configure(mode="determinate")
        self.set(0)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class FracturedKeyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Fractured Key")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(fg_color=Colors.BG_DARK)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"1200x800+{x}+{y}")

        self.selected_images = []
        self.current_tab = "encrypt"
        self._show_landing = True

        # Global, under-cursor smooth scrolling (Linux touchpad friendly)
        self._setup_global_scrolling()

        # High-visibility icon images for Linux (no emoji/font dependency)
        self._init_icon_images()

        # Root stack: landing page OR main app
        self.root_stack = ctk.CTkFrame(self, fg_color="transparent")
        self.root_stack.pack(fill="both", expand=True)

        # Landing page (shown first)
        self._create_landing_page()
        self.landing_frame.pack(fill="both", expand=True)

        # Main app container (header + sidebar + content + status)
        self.main_container = ctk.CTkFrame(self.root_stack, fg_color="transparent")
        # Don't pack yet — user must click Get Started / Login / Explore Features

        self._create_layout()
        self._create_header()
        self._create_sidebar()
        self._create_main_content()
        self._create_status_bar()

        self._show_tab("encrypt")

    def _setup_global_scrolling(self):
        """
        Route scroll events to the scrollable container under the cursor.
        This makes touchpad scrolling coordinate correctly with the visible scrollbar on Linux.
        """
        def find_scroll_canvas(widget):
            w = widget
            # Walk up the widget tree looking for a CTkScrollableFrame (has _parent_canvas)
            for _ in range(30):
                if w is None:
                    break
                # Only treat a tkinter Canvas as scroll-target if it's actually scrollable.
                # (Avoid decorative canvases like PixelatedCard border overlays, which caused "container moving".)
                try:
                    if isinstance(w, Canvas) and hasattr(w, "yview_scroll"):
                        ycmd = ""
                        try:
                            ycmd = str(w.cget("yscrollcommand") or "")
                        except Exception:
                            ycmd = ""
                        if ycmd.strip():
                            return w
                except Exception:
                    pass
                # CustomTkinter scrollable frame
                try:
                    if isinstance(w, ctk.CTkScrollableFrame):
                        return getattr(w, "_parent_canvas", None)
                except Exception:
                    pass
                if hasattr(w, "_parent_canvas"):
                    try:
                        return w._parent_canvas
                    except Exception:
                        return None
                try:
                    w = w.master
                except Exception:
                    break
            return None

        def wheel_units_from_event(event):
            d = getattr(event, "delta", 0) or 0
            if d == 0:
                return 0
            # Windows/Mac usually send ±120; Linux touchpads often send smaller values.
            if abs(d) >= 120:
                return -1 * (d / 120.0) * 6.0
            # Small deltas: scale down to keep it controllable
            return -1 * (d / 15.0)

        def on_mousewheel(event):
            canvas = find_scroll_canvas(getattr(event, "widget", None))
            if not canvas:
                return
            units = wheel_units_from_event(event)
            if units:
                smooth_scroll(canvas, units, steps=14, delay_ms=7)
                return "break"

        def on_button4(event):
            canvas = find_scroll_canvas(getattr(event, "widget", None))
            if not canvas:
                return
            smooth_scroll(canvas, -10, steps=12, delay_ms=7)
            return "break"

        def on_button5(event):
            canvas = find_scroll_canvas(getattr(event, "widget", None))
            if not canvas:
                return
            smooth_scroll(canvas, 10, steps=12, delay_ms=7)
            return "break"

        try:
            # add="+" so we don't stomp other bindings
            self.bind_all("<MouseWheel>", on_mousewheel, add="+")
            self.bind_all("<Shift-MouseWheel>", on_mousewheel, add="+")
            # Linux (X11) wheel events
            self.bind_all("<Button-4>", on_button4, add="+")
            self.bind_all("<Button-5>", on_button5, add="+")
        except Exception:
            pass

    def _init_icon_images(self):
        """
        Create crisp icon images so they are clearly visible on Linux without relying on emoji fonts.
        """
        def make_img(draw_fn, color_hex, size=22, stroke=2):
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            draw_fn(d, size, stroke, color_hex)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

        def draw_lock(d, size, stroke, color):
            # body
            d.rectangle([6, 10, size-6, size-5], outline=color, width=stroke)
            # shackle
            d.arc([6, 2, size-6, 14], start=0, end=180, fill=color, width=stroke)
            d.line([6, 10, 6, 11], fill=color, width=stroke)
            d.line([size-6, 10, size-6, 11], fill=color, width=stroke)

        def draw_unlock(d, size, stroke, color):
            d.rectangle([6, 10, size-6, size-5], outline=color, width=stroke)
            # open shackle (shifted right)
            d.arc([8, 2, size-4, 14], start=200, end=360, fill=color, width=stroke)
            d.line([8, 8, 8, 10], fill=color, width=stroke)

        def draw_folder(d, size, stroke, color):
            d.rectangle([3, 7, size-3, size-4], outline=color, width=stroke)
            d.rectangle([3, 5, 10, 7], outline=color, width=stroke)

        def draw_key(d, size, stroke, color):
            # key head
            d.ellipse([3, 7, 10, 14], outline=color, width=stroke)
            # key stem
            d.line([10, 11, size-3, 11], fill=color, width=stroke)
            # teeth
            d.line([size-7, 11, size-7, 15], fill=color, width=stroke)
            d.line([size-5, 11, size-5, 13], fill=color, width=stroke)

        def draw_info(d, size, stroke, color):
            d.ellipse([3, 3, size-3, size-3], outline=color, width=stroke)
            d.line([size//2, 9, size//2, size-7], fill=color, width=stroke)
            d.ellipse([size//2 - 1, 6, size//2 + 1, 8], fill=color, outline=color)

        def draw_shuffle(d, size, stroke, color):
            # Two crossing arrows
            d.line([4, 7, size-8, size-7], fill=color, width=stroke)
            d.line([4, size-7, size-8, 7], fill=color, width=stroke)
            # Arrow heads
            d.polygon([(size-8, size-7), (size-11, size-9), (size-11, size-5)], outline=color, fill=None)
            d.polygon([(size-8, 7), (size-11, 5), (size-11, 9)], outline=color, fill=None)

        def draw_image(d, size, stroke, color):
            d.rectangle([4, 5, size-4, size-5], outline=color, width=stroke)
            d.polygon([(6, size-7), (10, size-11), (14, size-9), (size-6, size-7)], outline=color, fill=None)
            d.ellipse([size-10, 8, size-7, 11], outline=color, width=stroke)

        def draw_offline(d, size, stroke, color):
            # Circle with slash
            d.ellipse([4, 4, size-4, size-4], outline=color, width=stroke)
            d.line([7, size-7, size-7, 7], fill=color, width=stroke)

        def draw_shield(d, size, stroke, color):
            # Simple shield outline
            d.polygon(
                [(size//2, 3), (size-5, 6), (size-6, size-9), (size//2, size-4), (6, size-9), (5, 6)],
                outline=color,
                fill=None
            )

        def draw_gear(d, size, stroke, color):
            # Simple gear: outer circle + inner circle + 4 teeth
            d.ellipse([5, 5, size-5, size-5], outline=color, width=stroke)
            d.ellipse([9, 9, size-9, size-9], outline=color, width=stroke)
            # teeth
            d.line([size//2, 2, size//2, 6], fill=color, width=stroke)
            d.line([size//2, size-6, size//2, size-2], fill=color, width=stroke)
            d.line([2, size//2, 6, size//2], fill=color, width=stroke)
            d.line([size-6, size//2, size-2, size//2], fill=color, width=stroke)

        # Two states for nav: muted + active (so visibility is good on Linux)
        muted = Colors.TEXT_SECONDARY
        active = Colors.ACCENT_PRIMARY

        self._nav_icon_images = {
            "encrypt": {
                "muted": make_img(draw_lock, muted),
                "active": make_img(draw_lock, active),
            },
            "decrypt": {
                "muted": make_img(draw_unlock, muted),
                "active": make_img(draw_unlock, active),
            },
            "manual": {
                "muted": make_img(draw_folder, muted),
                "active": make_img(draw_folder, active),
            },
            "about": {
                "muted": make_img(draw_info, muted),
                "active": make_img(draw_info, active),
            },
            "header": make_img(draw_lock, active, size=24, stroke=2),
            "key": {
                "muted": make_img(draw_key, muted),
                "active": make_img(draw_key, active),
            },
            # Extra icons for intro/landing page (avoid emoji -> no "?" on Linux)
            "shuffle": {
                "muted": make_img(draw_shuffle, muted),
                "active": make_img(draw_shuffle, active),
            },
            "image": {
                "muted": make_img(draw_image, muted),
                "active": make_img(draw_image, active),
            },
            "offline": {
                "muted": make_img(draw_offline, muted),
                "active": make_img(draw_offline, active),
            },
            "shield": {
                "muted": make_img(draw_shield, muted),
                "active": make_img(draw_shield, active),
            },
            "settings": {
                "muted": make_img(draw_gear, muted),
                "active": make_img(draw_gear, active),
            },
        }

    def _create_landing_page(self):
        """Attractive, interactive Introduction / Landing Page"""
        self.landing_frame = ctk.CTkFrame(
            self.root_stack,
            fg_color=Colors.BG_DARK,
            corner_radius=0
        )

        # Top accent strip (light blue theme)
        top_bar = ctk.CTkFrame(
            self.landing_frame,
            fg_color=Colors.ACCENT_MUTED,
            height=8,
            corner_radius=0
        )
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        inner = ctk.CTkScrollableFrame(
            self.landing_frame,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_LIGHT,
            scrollbar_button_hover_color=Colors.BG_HOVER
        )
        inner.pack(fill="both", expand=True, padx=48, pady=40)
        
        # Enable touchpad/mouse wheel scrolling
        enable_touchpad_scrolling(inner)

        # Widgets revealed with animation (do not pack yet)
        self._landing_reveal = []

        # Hero section — wrapped in a pixelated card
        hero_card = PixelatedCard(inner)
        hero_card_inner = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_card_inner.pack(fill="x", padx=40, pady=36)

        # Large hero title
        hero_label = ctk.CTkLabel(
            hero_card_inner,
            text="Fractured Key",
            font=Fonts.HERO,
            text_color=Colors.TEXT_PRIMARY
        )
        hero_label.pack(anchor="center", pady=(0, 14))

        # Accent line (light blue)
        underline = ctk.CTkFrame(
            hero_card_inner,
            fg_color=Colors.ACCENT_PRIMARY,
            height=4,
            width=140,
            corner_radius=2
        )
        underline.pack(anchor="center", pady=(0, 18))

        # Tagline — more prominent
        tagline = ctk.CTkLabel(
            hero_card_inner,
            text="A next-generation secure authentication system",
            font=Fonts.TAGLINE,
            text_color=Colors.TEXT_ACCENT
        )
        tagline.pack(anchor="center", pady=(0, 20))

        # Short engaging description
        desc_text = (
            "Split your secrets across multiple carriers. Military-grade encryption, "
            "Shamir Secret Sharing, and steganography — your credentials are never in one place. "
            "Recover only when you have enough fragments and your master password."
        )
        desc = ctk.CTkLabel(
            hero_card_inner,
            text=desc_text,
            font=Fonts.BODY_LG,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=640,
            justify="center"
        )
        desc.pack(anchor="center", pady=(0, 12))

        # Bullet highlights (inline, interactive feel)
        bullets = ctk.CTkLabel(
            hero_card_inner,
            text="AES-256-GCM  ·  Argon2id  ·  LSB steganography  ·  Offline-first",
            font=Fonts.BODY_SM,
            text_color=Colors.TEXT_MUTED
        )
        bullets.pack(anchor="center", pady=(0, 28))

        # CTA buttons — Get Started (primary), Explore Features (secondary). No Login.
        cta_frame = ctk.CTkFrame(hero_card_inner, fg_color="transparent")
        cta_frame.pack(anchor="center", pady=(0, 8))

        btn_get_started = AccentButton(
            cta_frame,
            text="  Get Started  ",
            command=lambda: self._enter_app("encrypt"),
            height=54,
            width=200
        )
        btn_get_started.pack(side="left", padx=12)

        btn_explore = SecondaryButton(
            cta_frame,
            text="  Explore Features  ",
            command=lambda: self._enter_app("about"),
            height=50,
            width=200
        )
        btn_explore.pack(side="left", padx=12)

        # Section divider with label (no pack — animated)
        section_label = ctk.CTkLabel(
            inner,
            text="Why Fractured Key",
            font=Fonts.TITLE_MD,
            text_color=Colors.TEXT_PRIMARY
        )

        hint = ctk.CTkLabel(
            inner,
            text="Scroll to explore features",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED
        )

        # Feature cards — more attractive layout with consistent hover (GlowingCard)
        features_container = ctk.CTkFrame(inner, fg_color="transparent")

        features = [
            ("encrypt", "Military-grade encryption", "AES-256-GCM + Argon2id key derivation"),
            ("shuffle", "Fragmented secrets", "Shamir Secret Sharing — partial fragments recover the whole"),
            ("image", "Hidden in plain sight", "LSB steganography embeds data inside images"),
            ("offline", "Offline-first", "No cloud dependency; everything stays on your device"),
            ("shield", "Recovery by design", "Only enough fragments + master password to decrypt"),
        ]

        for icon_key, title, desc in features:
            card = GlowingCard(features_container)
            card.pack(fill="x", pady=10, padx=16)
            card_inner = ctk.CTkFrame(card, fg_color="transparent")
            card_inner.pack(fill="x", padx=28, pady=22)

            # Linux-safe icon (image) — avoid emoji "?" on intro page
            icon_img = self._nav_icon_images.get(icon_key, {}).get("active") if isinstance(self._nav_icon_images.get(icon_key), dict) else None
            if icon_img is None:
                # fallback to known keys
                icon_img = self._nav_icon_images.get("about", {}).get("active")
            ctk.CTkLabel(
                card_inner,
                text="",
                image=icon_img
            ).pack(anchor="w", pady=(0, 12))

            ctk.CTkLabel(
                card_inner,
                text=title,
                font=Fonts.TITLE_SM,
                text_color=Colors.TEXT_PRIMARY
            ).pack(anchor="w", pady=(0, 6))
            ctk.CTkLabel(
                card_inner,
                text=desc,
                font=Fonts.BODY_SM,
                text_color=Colors.TEXT_MUTED,
                wraplength=560,
                justify="left"
            ).pack(anchor="w")

        # Footer (no pack — animated)
        footer = ctk.CTkLabel(
            inner,
            text="Secure · Offline · Portfolio-ready",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED
        )

        # Staggered reveal animation: pack widgets in sequence
        self._landing_reveal = [
            (hero_card, {"fill": "x", "pady": (24, 32), "padx": 24}),
            (section_label, {"anchor": "center", "pady": (36, 8)}),
            (hint, {"anchor": "center", "pady": (0, 20)}),
            (features_container, {"fill": "x", "pady": (0, 28)}),
            (footer, {"anchor": "center", "pady": (24, 28)}),
        ]
        self.after(180, lambda: self._reveal_next_landing(0))

    def _reveal_next_landing(self, i):
        """Reveal next landing section (staggered animation)."""
        if i < len(self._landing_reveal):
            widget, kwargs = self._landing_reveal[i]
            widget.pack(**kwargs)
            self.after(130, lambda: self._reveal_next_landing(i + 1))

    def _enter_app(self, tab_id="encrypt"):
        """Switch from landing page to main app and optionally open a tab."""
        if not self._show_landing:
            return
        self._show_landing = False
        self.landing_frame.pack_forget()
        self.main_container.pack(fill="both", expand=True)
        self._show_tab(tab_id)

    def _show_landing_page(self):
        """Return from main app to the Introduction / Landing page and replay animation."""
        if self._show_landing:
            return
        self._show_landing = True
        self.main_container.pack_forget()
        self.landing_frame.pack(fill="both", expand=True)
        # Unpack sections so staggered reveal animation runs again
        for widget, _ in self._landing_reveal:
            try:
                widget.pack_forget()
            except Exception:
                pass
        self.after(120, lambda: self._reveal_next_landing(0))

    def _create_layout(self):
        """Main app layout structure"""
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
    def _create_header(self):
        """Create the app header - premium blue theme"""
        header = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_DARKEST,
            height=72,
            corner_radius=0,
            border_width=0
        )
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=28, pady=14)

        icon_label = ctk.CTkLabel(
            title_frame,
            text="",
            image=self._nav_icon_images["header"]
        )
        icon_label.pack(side="left", padx=(0, 14))

        title_text = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_text.pack(side="left")

        ctk.CTkLabel(
            title_text,
            text="Fractured Key",
            font=Fonts.TITLE_LG,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_text,
            text="Secure authentication · Steganographic vault",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED
        ).pack(anchor="w")

        # Right side: Back to Introduction + version
        header_right = ctk.CTkFrame(header, fg_color="transparent")
        header_right.pack(side="right", padx=28, pady=14)

        btn_intro = SecondaryButton(
            header_right,
            text="  Back to Introduction  ",
            command=self._show_landing_page,
            height=40,
            width=180
        )
        btn_intro.pack(side="left", padx=(0, 12))

        version_badge = ctk.CTkLabel(
            header_right,
            text=" v2.0 ",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
            fg_color=Colors.BG_LIGHT,
            corner_radius=8,
            padx=12,
            pady=5
        )
        version_badge.pack(side="left")
        
    def _create_sidebar(self):
        """Create the navigation sidebar - clean, modern"""
        sidebar = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_DARKEST,
            width=260,
            corner_radius=0,
            border_width=0
        )
        sidebar.grid(row=1, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", pady=24, padx=16)

        nav_items = [
            ("encrypt", Colors.ICON_LOCK, "Encrypt", "Hide your secrets"),
            ("decrypt", Colors.ICON_UNLOCK, "Decrypt", "Reveal your secrets"),
            ("manual", Colors.ICON_FOLDER, "Manual", "Direct file decrypt"),
            ("about", Colors.ICON_INFO, "About", "Learn more"),
        ]

        self.nav_buttons = {}

        for tab_id, icon, title, subtitle in nav_items:
            btn_frame = ctk.CTkFrame(
                nav_frame,
                fg_color="transparent",
                corner_radius=12,
                cursor="hand2"
            )
            btn_frame.pack(fill="x", pady=6)

            btn_frame.bind("<Button-1>", lambda e, t=tab_id: self._show_tab(t))

            content = ctk.CTkFrame(btn_frame, fg_color="transparent")
            content.pack(fill="x", padx=14, pady=12)
            content.bind("<Button-1>", lambda e, t=tab_id: self._show_tab(t))

            icon_lbl = ctk.CTkLabel(
                content,
                text="",
                image=self._nav_icon_images[tab_id]["muted"]
            )
            icon_lbl.pack(side="left", padx=(0, 14))
            icon_lbl.bind("<Button-1>", lambda e, t=tab_id: self._show_tab(t))

            text_container = ctk.CTkFrame(content, fg_color="transparent")
            text_container.pack(side="left", fill="x", expand=True)
            text_container.bind("<Button-1>", lambda e, t=tab_id: self._show_tab(t))

            title_lbl = ctk.CTkLabel(
                text_container,
                text=title,
                font=Fonts.TITLE_SM,
                text_color=Colors.TEXT_PRIMARY,
                anchor="w"
            )
            title_lbl.pack(anchor="w")
            title_lbl.bind("<Button-1>", lambda e, t=tab_id: self._show_tab(t))

            subtitle_lbl = ctk.CTkLabel(
                text_container,
                text=subtitle,
                font=Fonts.CAPTION,
                text_color=Colors.TEXT_MUTED,
                anchor="w"
            )
            subtitle_lbl.pack(anchor="w")
            subtitle_lbl.bind("<Button-1>", lambda e, t=tab_id: self._show_tab(t))

            self.nav_buttons[tab_id] = {
                "frame": btn_frame,
                "icon": icon_lbl,
                "title": title_lbl,
                "subtitle": subtitle_lbl
            }

            def on_enter(e, f=btn_frame, t=tab_id):
                if self.current_tab != t:
                    f.configure(fg_color=Colors.BG_HOVER)

            def on_leave(e, f=btn_frame, t=tab_id):
                if self.current_tab != t:
                    f.configure(fg_color="transparent")

            btn_frame.bind("<Enter>", on_enter)
            btn_frame.bind("<Leave>", on_leave)

        divider = ctk.CTkFrame(sidebar, fg_color=Colors.BORDER, height=1)
        divider.pack(fill="x", padx=16, pady=24)

        security_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        security_frame.pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(
            security_frame,
            text="Security",
            image=self._nav_icon_images["shield"]["muted"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 10))

        security_items = [
            "AES-256-GCM Encryption",
            "Argon2id Key Derivation",
            "Shamir Secret Sharing",
            "LSB Steganography"
        ]

        for item in security_items:
            item_frame = ctk.CTkFrame(security_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=4)

            ctk.CTkLabel(
                item_frame,
                text="•",
                font=Fonts.BODY_SM,
                text_color=Colors.BLUE_GLOW
            ).pack(side="left", padx=(0, 10))

            ctk.CTkLabel(
                item_frame,
                text=item,
                font=Fonts.BODY_SM,
                text_color=Colors.TEXT_MUTED
            ).pack(side="left")
            
    def _create_main_content(self):
        """Create the main content area"""
        # Content container
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_DARK,
            corner_radius=0
        )
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        
        # Create all tab frames
        self.tabs = {}
        self.tabs["encrypt"] = self._create_encrypt_tab()
        self.tabs["decrypt"] = self._create_decrypt_tab()
        self.tabs["manual"] = self._create_manual_tab()
        self.tabs["about"] = self._create_about_tab()
        
    def _create_encrypt_tab(self):
        """Create the encryption tab"""
        tab = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_LIGHT,
            scrollbar_button_hover_color=Colors.BG_HOVER
        )
        enable_touchpad_scrolling(tab)
        
        # Page title - consistent spacing
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=44, pady=(36, 24))
        
        ctk.CTkLabel(
            header_frame,
            text="Encrypt Password",
            font=Fonts.TITLE_LG,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame,
            text="Secure your password using military-grade encryption and steganography",
            font=Fonts.BODY_MD,
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w", pady=(8, 0))
        
        content = ctk.CTkFrame(tab, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=44, pady=(0, 36))
        
        # Password input card
        password_card = GlowingCard(content)
        password_card.pack(fill="x", pady=(0, 20))
        
        card_content = ctk.CTkFrame(password_card, fg_color="transparent")
        card_content.pack(fill="x", padx=24, pady=24)
        
        # Password to encrypt
        ctk.CTkLabel(
            card_content,
            text="Password to Encrypt",
            image=self._nav_icon_images["key"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 8))
        
        self.encrypt_password_entry = ModernEntry(
            card_content,
            placeholder="Enter the password you want to protect...",
            is_password=True,
            width=500
        )
        self.encrypt_password_entry.pack(fill="x", pady=(0, 20))
        
        # Master password
        ctk.CTkLabel(
            card_content,
            text="Master Password",
            image=self._nav_icon_images["encrypt"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 8))
        
        self.encrypt_master_entry = ModernEntry(
            card_content,
            placeholder="Enter your master password...",
            is_password=True,
            width=500
        )
        self.encrypt_master_entry.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(
            card_content,
            text="This password will be used to decrypt your data later",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED
        ).pack(anchor="w")
        
        # Options card
        options_card = GlowingCard(content)
        options_card.pack(fill="x", pady=(0, 20))
        
        options_content = ctk.CTkFrame(options_card, fg_color="transparent")
        options_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            options_content,
            text="Encryption Options",
            image=self._nav_icon_images["settings"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 15))
        
        self.use_shares_var = ctk.BooleanVar(value=True)
        
        shares_checkbox = ctk.CTkCheckBox(
            options_content,
            text="Split into 3 shares and embed into images",
            variable=self.use_shares_var,
            font=Fonts.BODY_MD,
            text_color=Colors.TEXT_PRIMARY,
            fg_color=Colors.ACCENT_PRIMARY,
            hover_color=Colors.ACCENT_GLOW,
            border_color=Colors.BORDER,
            checkmark_color=Colors.BG_DARKEST,
            corner_radius=6
        )
        shares_checkbox.pack(anchor="w", pady=(0, 8))
        
        ctk.CTkLabel(
            options_content,
            text="💡 Creates 3 stego images. You need at least 2 to decrypt.",  # Keep emoji for info text
            font=Fonts.BODY_SM,
            text_color=Colors.TEXT_MUTED
        ).pack(anchor="w", padx=(26, 0))
        
        # Action button
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        self.encrypt_btn = AccentButton(
            button_frame,
            text="Start Encryption",
            image=self._nav_icon_images["encrypt"]["active"],
            compound="left",
            command=self._start_encryption,
            width=220
        )
        self.encrypt_btn.pack(anchor="w")
        
        # Progress
        self.encrypt_progress = AnimatedProgress(content)
        self.encrypt_progress.pack(fill="x", pady=(0, 20))
        
        # Output card
        output_card = GlowingCard(content)
        output_card.pack(fill="both", expand=True)
        
        output_header = ctk.CTkFrame(output_card, fg_color="transparent")
        output_header.pack(fill="x", padx=24, pady=(24, 12))
        
        ctk.CTkLabel(
            output_header,
            text="Output Log",
            image=self._nav_icon_images["manual"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(side="left")
        
        # Clear button
        SecondaryButton(
            output_header,
            text="Clear",
            command=lambda: self.encrypt_output.delete("1.0", "end"),
            width=80,
            height=32
        ).pack(side="right")
        
        self.encrypt_output = ModernTextbox(output_card, height=200)
        self.encrypt_output.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        
        # Initial message
        self.encrypt_output.insert("1.0", f"{Colors.ICON_LOCK} Ready to encrypt your password.\n")
        self.encrypt_output.insert("end", "━" * 50 + "\n")
        self.encrypt_output.insert("end", "Enter your password and master password above, then click 'Start Encryption'.\n")
        
        return tab
        
    def _create_decrypt_tab(self):
        """Create the decryption tab"""
        tab = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_LIGHT,
            scrollbar_button_hover_color=Colors.BG_HOVER
        )
        enable_touchpad_scrolling(tab)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=44, pady=(36, 24))
        
        ctk.CTkLabel(
            header_frame,
            text="Decrypt Password",
            font=Fonts.TITLE_LG,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame,
            text="Recover your password from steganographic images",
            font=Fonts.BODY_MD,
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w", pady=(8, 0))
        
        content = ctk.CTkFrame(tab, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=44, pady=(0, 36))
        
        # Instructions card
        instructions_card = GlowingCard(content)
        instructions_card.pack(fill="x", pady=(0, 20))
        
        instructions_content = ctk.CTkFrame(instructions_card, fg_color="transparent")
        instructions_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            instructions_content,
            text="How to Decrypt",
            image=self._nav_icon_images["about"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 12))
        
        steps = [
            ("1", "Select at least 2 stego images from the same encryption session"),
            ("2", "Enter your master password"),
            ("3", "Click 'Start Decryption' to recover your password")
        ]
        
        for num, text in steps:
            step_frame = ctk.CTkFrame(instructions_content, fg_color="transparent")
            step_frame.pack(fill="x", pady=4)
            
            ctk.CTkLabel(
                step_frame,
                text=num,
                font=Fonts.BODY_SM,
                text_color=Colors.BG_DARKEST,
                fg_color=Colors.ACCENT_PRIMARY,
                corner_radius=10,
                width=24,
                height=24
            ).pack(side="left", padx=(0, 12))
            
            ctk.CTkLabel(
                step_frame,
                text=text,
                font=Fonts.BODY_MD,
                text_color=Colors.TEXT_SECONDARY
            ).pack(side="left")
        
        # Image selection card
        image_card = GlowingCard(content)
        image_card.pack(fill="x", pady=(0, 20))
        
        image_content = ctk.CTkFrame(image_card, fg_color="transparent")
        image_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            image_content,
            text="Selected Images",
            image=self._nav_icon_images["manual"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 12))
        
        # Image list
        list_frame = ctk.CTkFrame(
            image_content,
            fg_color=Colors.BG_DARKEST,
            corner_radius=10,
            border_width=1,
            border_color=Colors.BORDER
        )
        list_frame.pack(fill="x", pady=(0, 12))
        
        self.image_listbox = ctk.CTkTextbox(
            list_frame,
            height=120,
            fg_color=Colors.BG_DARKEST,
            text_color=Colors.TEXT_PRIMARY,
            font=Fonts.MONO_MD,
            state="disabled",
            corner_radius=10,
            border_width=0
        )
        self.image_listbox.pack(fill="x", padx=4, pady=4)
        
        # Image buttons
        btn_frame = ctk.CTkFrame(image_content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        SuccessButton(
            btn_frame,
            text="Add Image",
            image=self._nav_icon_images["manual"]["active"],
            compound="left",
            command=self._add_image_file,
            width=140,
            height=40
        ).pack(side="left", padx=(0, 10))
        
        DangerButton(
            btn_frame,
            text="Remove Selected",
            # keep no-image here; destructive actions often look cleaner without an icon
            command=self._remove_all_images,
            width=160,
            height=40
        ).pack(side="left")
        
        # Master password card
        password_card = GlowingCard(content)
        password_card.pack(fill="x", pady=(0, 20))
        
        password_content = ctk.CTkFrame(password_card, fg_color="transparent")
        password_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            password_content,
            text="Master Password",
            image=self._nav_icon_images["encrypt"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 8))
        
        self.decrypt_master_entry = ModernEntry(
            password_content,
            placeholder="Enter your master password...",
            is_password=True,
            width=500
        )
        self.decrypt_master_entry.pack(fill="x")
        
        # Action button
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        self.decrypt_btn = SuccessButton(
            button_frame,
            text="Start Decryption",
            image=self._nav_icon_images["decrypt"]["active"],
            compound="left",
            command=self._start_decryption,
            width=220
        )
        self.decrypt_btn.pack(anchor="w")
        
        # Progress
        self.decrypt_progress = AnimatedProgress(content)
        self.decrypt_progress.pack(fill="x", pady=(0, 20))
        
        # Output card
        output_card = GlowingCard(content)
        output_card.pack(fill="both", expand=True)
        
        output_header = ctk.CTkFrame(output_card, fg_color="transparent")
        output_header.pack(fill="x", padx=24, pady=(24, 12))
        
        ctk.CTkLabel(
            output_header,
            text="Decryption Results",
            image=self._nav_icon_images["manual"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(side="left")
        
        SecondaryButton(
            output_header,
            text="Clear",
            command=lambda: self.decrypt_output.delete("1.0", "end"),
            width=80,
            height=32
        ).pack(side="right")
        
        self.decrypt_output = ModernTextbox(output_card, height=200)
        self.decrypt_output.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        
        # Initial message
        self.decrypt_output.insert("1.0", "🔓 Ready to decrypt your password.\n")
        self.decrypt_output.insert("end", "━" * 50 + "\n")
        self.decrypt_output.insert("end", "Select at least 2 stego images and enter your master password.\n")
        
        return tab
        
    def _create_manual_tab(self):
        """Create the manual decryption tab"""
        tab = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_LIGHT,
            scrollbar_button_hover_color=Colors.BG_HOVER
        )
        enable_touchpad_scrolling(tab)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=44, pady=(36, 24))
        
        ctk.CTkLabel(
            header_frame,
            text="Manual Decryption",
            font=Fonts.TITLE_LG,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame,
            text="Decrypt .bin files directly without steganography",
            font=Fonts.BODY_MD,
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w", pady=(8, 0))
        
        content = ctk.CTkFrame(tab, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=44, pady=(0, 36))
        
        # File selection card
        file_card = GlowingCard(content)
        file_card.pack(fill="x", pady=(0, 20))
        
        file_content = ctk.CTkFrame(file_card, fg_color="transparent")
        file_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            file_content,
            text="Select Binary File",
            image=self._nav_icon_images["manual"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 12))
        
        file_input_frame = ctk.CTkFrame(file_content, fg_color="transparent")
        file_input_frame.pack(fill="x")
        
        self.manual_file_entry = ModernEntry(
            file_input_frame,
            placeholder="Select a .bin file...",
            width=400
        )
        self.manual_file_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        
        SecondaryButton(
            file_input_frame,
            text="Browse",
            image=self._nav_icon_images["manual"]["active"],
            compound="left",
            command=self._browse_manual_file,
            width=110,
            height=48
        ).pack(side="right")
        
        # Master password card
        password_card = GlowingCard(content)
        password_card.pack(fill="x", pady=(0, 20))
        
        password_content = ctk.CTkFrame(password_card, fg_color="transparent")
        password_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            password_content,
            text="Master Password",
            image=self._nav_icon_images["encrypt"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 8))
        
        self.manual_master_entry = ModernEntry(
            password_content,
            placeholder="Enter your master password...",
            is_password=True,
            width=500
        )
        self.manual_master_entry.pack(fill="x")
        
        # Action button
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        self.manual_decrypt_btn = SuccessButton(
            button_frame,
            text="Decrypt File",
            image=self._nav_icon_images["decrypt"]["active"],
            compound="left",
            command=self._start_manual_decryption,
            width=180
        )
        self.manual_decrypt_btn.pack(anchor="w")
        
        # Output card
        output_card = GlowingCard(content)
        output_card.pack(fill="both", expand=True)
        
        output_header = ctk.CTkFrame(output_card, fg_color="transparent")
        output_header.pack(fill="x", padx=24, pady=(24, 12))
        
        ctk.CTkLabel(
            output_header,
            text="Results",
            image=self._nav_icon_images["manual"]["active"],
            compound="left",
            font=Fonts.LABEL,
            text_color=Colors.TEXT_PRIMARY
        ).pack(side="left")
        
        SecondaryButton(
            output_header,
            text="Clear",
            command=lambda: self.manual_output.delete("1.0", "end"),
            width=80,
            height=32
        ).pack(side="right")
        
        self.manual_output = ModernTextbox(output_card, height=250)
        self.manual_output.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        
        # Initial message
        self.manual_output.insert("1.0", "🔓 Manual decryption mode.\n")
        self.manual_output.insert("end", "━" * 50 + "\n")
        self.manual_output.insert("end", "Use this if you saved encrypted data as a .bin file.\n")
        
        return tab
        
    def _create_about_tab(self):
        """Create the about tab"""
        tab = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_LIGHT,
            scrollbar_button_hover_color=Colors.BG_HOVER
        )
        enable_touchpad_scrolling(tab)
        
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=44, pady=(36, 24))
        
        ctk.CTkLabel(
            header_frame,
            text="About Fractured Key",
            font=Fonts.TITLE_LG,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w")
        
        content = ctk.CTkFrame(tab, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=44, pady=(0, 36))
        
        # Overview card
        overview_card = GlowingCard(content)
        overview_card.pack(fill="x", pady=(0, 20))
        
        overview_content = ctk.CTkFrame(overview_card, fg_color="transparent")
        overview_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            overview_content,
            text="What is Fractured Key?",
            image=self._nav_icon_images["about"]["active"],
            compound="left",
            font=Fonts.TITLE_MD,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 12))
        
        overview_text = """Fractured Key is an experimental approach to secure credential storage that avoids traditional single-point vaults. Instead of keeping an encrypted blob in one place, your data is divided, transformed, and distributed across multiple independent carriers.

The result is a system that doesn't resemble a password manager in its raw form — the stored material does not look like secrets at all."""
        
        ctk.CTkLabel(
            overview_content,
            text=overview_text,
            font=Fonts.BODY_MD,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=700,
            justify="left"
        ).pack(anchor="w")
        
        # How it works card
        how_card = GlowingCard(content)
        how_card.pack(fill="x", pady=(0, 20))
        
        how_content = ctk.CTkFrame(how_card, fg_color="transparent")
        how_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            how_content,
            text="How It Works",
            image=self._nav_icon_images["shuffle"]["active"],
            compound="left",
            font=Fonts.TITLE_MD,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 16))
        
        steps = [
            ("1", "Your password is encrypted with AES-GCM using a master password"),
            ("2", "The encrypted data is split into shares using Shamir Secret Sharing"),
            ("3", "Each share is embedded into a different image using steganography"),
            ("4", "You need at least 2 out of 3 images to reconstruct your password")
        ]
        
        for num, text in steps:
            step_frame = ctk.CTkFrame(how_content, fg_color="transparent")
            step_frame.pack(fill="x", pady=6)
            
            ctk.CTkLabel(
                step_frame,
                text=num,
                font=Fonts.BODY_MD,
                text_color=Colors.BG_DARKEST,
                fg_color=Colors.ACCENT_PRIMARY,
                corner_radius=12,
                width=28,
                height=28
            ).pack(side="left", padx=(0, 16))
            
            ctk.CTkLabel(
                step_frame,
                text=text,
                font=Fonts.BODY_MD,
                text_color=Colors.TEXT_SECONDARY
            ).pack(side="left")
        
        # Features card
        features_card = GlowingCard(content)
        features_card.pack(fill="x", pady=(0, 20))
        
        features_content = ctk.CTkFrame(features_card, fg_color="transparent")
        features_content.pack(fill="x", padx=24, pady=24)
        
        ctk.CTkLabel(
            features_content,
            text="Key Features",
            image=self._nav_icon_images["shield"]["active"],
            compound="left",
            font=Fonts.TITLE_MD,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 16))
        
        features = [
            ("encrypt", "Offline Security", "No reliance on online services"),
            ("shuffle", "Redundancy", "Only partial components needed to recover"),
            ("image", "Steganographic", "Information hidden where least expected"),
            ("shield", "Layered Crypto", "Multiple primitives combined for security")
        ]
        
        features_grid = ctk.CTkFrame(features_content, fg_color="transparent")
        features_grid.pack(fill="x")
        
        for i, (icon_key, title, desc) in enumerate(features):
            feature_frame = ctk.CTkFrame(
                features_grid,
                fg_color=Colors.BG_LIGHT,
                corner_radius=12
            )
            feature_frame.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="ew")
            features_grid.grid_columnconfigure(i%2, weight=1)
            
            inner = ctk.CTkFrame(feature_frame, fg_color="transparent")
            inner.pack(fill="x", padx=16, pady=16)
            
            icon_img = self._nav_icon_images.get(icon_key, {}).get("active") if isinstance(self._nav_icon_images.get(icon_key), dict) else None
            if icon_img is None:
                icon_img = self._nav_icon_images.get("about", {}).get("active")
            ctk.CTkLabel(
                inner,
                text="",
                image=icon_img
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                inner,
                text=title,
                font=Fonts.TITLE_SM,
                text_color=Colors.TEXT_PRIMARY
            ).pack(anchor="w", pady=(8, 4))
            
            ctk.CTkLabel(
                inner,
                text=desc,
                font=Fonts.BODY_SM,
                text_color=Colors.TEXT_MUTED
            ).pack(anchor="w")
        
        # Warning card
        warning_card = ctk.CTkFrame(
            content,
            fg_color=Colors.BG_MEDIUM,
            corner_radius=16,
            border_width=1,
            border_color=Colors.WARNING
        )
        warning_card.pack(fill="x", pady=(0, 20))
        
        warning_content = ctk.CTkFrame(warning_card, fg_color="transparent")
        warning_content.pack(fill="x", padx=24, pady=24)
        
        warning_header = ctk.CTkFrame(warning_content, fg_color="transparent")
        warning_header.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(
            warning_header,
            text=Colors.ICON_WARNING,
            font=Fonts.EMOJI_SM,
            text_color=Colors.WARNING
        ).pack(side="left", padx=(0, 12))
        
        ctk.CTkLabel(
            warning_header,
            text="Disclaimer",
            font=Fonts.TITLE_SM,
            text_color=Colors.WARNING
        ).pack(side="left")
        
        ctk.CTkLabel(
            warning_content,
            text="This is research-driven software intended for educational and experimental use. Always maintain secure backups of important credentials.",
            font=Fonts.BODY_MD,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=700,
            justify="left"
        ).pack(anchor="w")
        
        return tab
        
    def _create_status_bar(self):
        """Create the status bar"""
        status_bar = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_DARKEST,
            height=36,
            corner_radius=0
        )
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)
        
        status_content = ctk.CTkFrame(status_bar, fg_color="transparent")
        status_content.pack(fill="both", expand=True, padx=20)
        
        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            status_content,
            text="●",
            font=Fonts.BODY_SM,
            text_color=Colors.SUCCESS
        )
        self.status_indicator.pack(side="left", padx=(0, 8))
        
        # Status text
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            status_content,
            textvariable=self.status_var,
            font=Fonts.BODY_SM,
            text_color=Colors.TEXT_MUTED
        )
        self.status_label.pack(side="left")
        
        ctk.CTkLabel(
            status_content,
            text="Fractured Key v2.0 · AES-256-GCM · Argon2id · SSS",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED
        ).pack(side="right")
        
    def _show_tab(self, tab_id):
        """Switch to a different tab"""
        # Update current tab
        self.current_tab = tab_id
        
        # Hide all tabs
        for tab in self.tabs.values():
            tab.pack_forget()
            
        # Show selected tab
        self.tabs[tab_id].pack(fill="both", expand=True)
        
        # Update navigation styling (blue accent for active)
        for btn_id, btn_info in self.nav_buttons.items():
            if btn_id == tab_id:
                btn_info["frame"].configure(fg_color=Colors.BG_LIGHT)
                btn_info["icon"].configure(image=self._nav_icon_images[btn_id]["active"])
                btn_info["title"].configure(text_color=Colors.ACCENT_PRIMARY)
                btn_info["subtitle"].configure(text_color=Colors.TEXT_SECONDARY)
            else:
                btn_info["frame"].configure(fg_color="transparent")
                btn_info["icon"].configure(image=self._nav_icon_images[btn_id]["muted"])
                btn_info["title"].configure(text_color=Colors.TEXT_PRIMARY)
                btn_info["subtitle"].configure(text_color=Colors.TEXT_MUTED)
                
    def _update_status(self, message, status_type="info"):
        """Update status bar"""
        self.status_var.set(message)
        
        if status_type == "success":
            self.status_indicator.configure(text_color=Colors.SUCCESS)
        elif status_type == "error":
            self.status_indicator.configure(text_color=Colors.ERROR)
        elif status_type == "warning":
            self.status_indicator.configure(text_color=Colors.WARNING)
        else:
            self.status_indicator.configure(text_color=Colors.ACCENT_PRIMARY)
            
    def _log_output(self, text_widget, message, msg_type="info"):
        """Add message to output text widget"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Format based on type
        prefix = ""
        if msg_type == "success":
            prefix = "✓"
        elif msg_type == "error":
            prefix = "✗"
        elif msg_type == "warning":
            prefix = "⚠"
        else:
            prefix = "▸"
            
        formatted = f"[{timestamp}] {prefix} {message}\n"
        text_widget.insert("end", formatted)
        text_widget.see("end")
        self.update_idletasks()
        
    # ═══════════════════════════════════════════════════════════════════════════
    # ENCRYPTION LOGIC
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _start_encryption(self):
        """Start the encryption process"""
        password = self.encrypt_password_entry.get().strip()
        master_password = self.encrypt_master_entry.get().strip()
        
        if not password:
            messagebox.showerror("Error", "Please enter a password to encrypt")
            return
            
        if not master_password:
            messagebox.showerror("Error", "Please enter a master password")
            return
            
        # Clear output
        self.encrypt_output.delete("1.0", "end")
        
        # Start animation
        self.encrypt_progress.start_animation()
        self.encrypt_btn.configure(state="disabled")
        self._update_status("Encrypting...", "info")
        
        # Run in thread
        thread = threading.Thread(
            target=self._encrypt_worker,
            args=(password, master_password)
        )
        thread.daemon = True
        thread.start()
        
    def _encrypt_worker(self, password, master_password):
        """Encryption worker thread"""
        try:
            self._log_output(self.encrypt_output, "Starting encryption process...", "info")
            self._log_output(self.encrypt_output, "━" * 50, "info")
            
            # Encrypt the password
            self._log_output(self.encrypt_output, f"Password length: {len(password)} characters", "info")
            self._log_output(self.encrypt_output, "Deriving key with Argon2id...", "info")
            
            salt, nonce, ciphertext_with_tag = encrypt_password_aes_gcm(password, master_password)
            
            import base64
            ciphertext = ciphertext_with_tag[:-16]
            auth_tag = ciphertext_with_tag[-16:]
            
            self._log_output(self.encrypt_output, "Encryption successful!", "success")
            self._log_output(self.encrypt_output, "━" * 50, "info")
            self._log_output(self.encrypt_output, f"Salt: {base64.b64encode(salt).decode()}", "info")
            self._log_output(self.encrypt_output, f"Nonce: {base64.b64encode(nonce).decode()}", "info")
            self._log_output(self.encrypt_output, f"Ciphertext: {base64.b64encode(ciphertext).decode()}", "info")
            self._log_output(self.encrypt_output, f"Auth Tag: {base64.b64encode(auth_tag).decode()}", "info")
            
            binary_blob = salt + nonce + ciphertext_with_tag
            
            if self.use_shares_var.get():
                self._log_output(self.encrypt_output, "━" * 50, "info")
                self._log_output(self.encrypt_output, "Splitting into SSS shares...", "info")
                self._create_shares_and_embed(binary_blob)
            else:
                filename = "encrypted_output.bin"
                with open(filename, "wb") as f:
                    f.write(binary_blob)
                abs_path = os.path.abspath(filename)
                self._log_output(self.encrypt_output, f"Binary file saved: {abs_path}", "success")
                # Also print to terminal so user sees the exact location
                try:
                    print(f"[Fractured Key] Binary file saved at: {abs_path}")
                except Exception:
                    pass
                
        except Exception as e:
            self._log_output(self.encrypt_output, f"Encryption failed: {str(e)}", "error")
        finally:
            self.after(0, self._encryption_finished)
            
    def _create_shares_and_embed(self, binary_blob):
        """Create shares and embed into images"""
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            
            self._log_output(self.encrypt_output, "Generating ephemeral key...", "info")
            K2 = os.urandom(16)
            aes = AESGCM(K2)
            nonce2 = os.urandom(12)
            packaged_ct_and_tag = aes.encrypt(nonce2, binary_blob, None)
            packaged_cipher = nonce2 + packaged_ct_and_tag
            
            n_shares = 3
            threshold = 2
            self._log_output(self.encrypt_output, f"Splitting key into {n_shares} shares (threshold: {threshold})...", "info")
            shares = split_bytes_into_shares(K2, n=n_shares, k=threshold)
            
            for i, share_bytes in enumerate(shares, start=1):
                self._log_output(self.encrypt_output, f"━" * 50, "info")
                self._log_output(self.encrypt_output, f"Processing share {i}/{n_shares}...", "info")
                
                file_types = [("Images", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
                carrier_path = native_file_dialog(
                    self,
                    title=f"Select carrier image for share {i}",
                    filetypes=file_types,
                    mode="open",
                    initialdir=os.path.expanduser("~/Pictures")
                )
                
                if not carrier_path:
                    self._log_output(self.encrypt_output, f"No carrier selected for share {i}. Skipping.", "warning")
                    continue
                    
                self._log_output(self.encrypt_output, f"Carrier: {os.path.basename(carrier_path)}", "info")
                
                payload = self._wrap_share_payload(share_bytes, index=i, total=n_shares,
                                                   threshold=threshold, packaged_cipher=packaged_cipher)
                
                output_path = native_file_dialog(
                    self,
                    title=f"Save stego image for share {i}",
                    filetypes=[("PNG image", "*.png"), ("All files", "*.*")],
                    mode="save",
                    initialdir=os.path.expanduser("~/Pictures"),
                    defaultextension=".png"
                )
                
                if not output_path:
                    base = os.path.splitext(carrier_path)[0]
                    output_path = f"{base}_stego_{i}.png"
                    
                saved_path = embed_data_into_image(carrier_path, payload, output_path=output_path)
                self._log_output(self.encrypt_output, f"Share {i} embedded: {saved_path}", "success")
                
            self._log_output(self.encrypt_output, "━" * 50, "info")
            self._log_output(self.encrypt_output, "All shares processed successfully!", "success")
            self._log_output(self.encrypt_output, "Keep at least 2 stego images safe!", "warning")
            
        except Exception as e:
            self._log_output(self.encrypt_output, f"Share creation failed: {str(e)}", "error")
            
    def _wrap_share_payload(self, share_bytes, index, total, threshold, packaged_cipher):
        """Wrap share payload with metadata"""
        SHARE_MAGIC = b"FKSS01"
        SHARE_VERSION = 1
        
        header = bytearray()
        header += SHARE_MAGIC
        header.append(SHARE_VERSION & 0xFF)
        header.append(index & 0xFF)
        header.append(total & 0xFF)
        header.append(threshold & 0xFF)
        header += len(share_bytes).to_bytes(4, 'big')
        header += len(packaged_cipher).to_bytes(4, 'big')
        return bytes(header) + share_bytes + packaged_cipher
        
    def _encryption_finished(self):
        """Called when encryption is finished — clear passwords so they are not shown."""
        self.encrypt_progress.stop_animation()
        self.encrypt_btn.configure(state="normal")
        self._update_status("Encryption completed", "success")
        self.encrypt_password_entry.delete(0, "end")
        self.encrypt_master_entry.delete(0, "end")
        
    # ═══════════════════════════════════════════════════════════════════════════
    # DECRYPTION LOGIC
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _add_image_file(self):
        """Add image file to decryption list"""
        file_types = [("Images", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
        file_path = native_file_dialog(
            self,
            title="Select stego image",
            filetypes=file_types,
            mode="open",
            initialdir=os.path.expanduser("~/Pictures")
        )
        
        if file_path and file_path not in self.selected_images:
            self.selected_images.append(file_path)
            self._update_image_list()
            
    def _remove_all_images(self):
        """Remove all selected images"""
        self.selected_images = []
        self._update_image_list()
        
    def _update_image_list(self):
        """Update the image list display"""
        self.image_listbox.configure(state="normal")
        self.image_listbox.delete("1.0", "end")
        
        if not self.selected_images:
            self.image_listbox.insert("1.0", "No images selected.\n")
        else:
            for i, path in enumerate(self.selected_images, 1):
                self.image_listbox.insert("end", f"{i}. {os.path.basename(path)}\n")
                
        self.image_listbox.configure(state="disabled")
        
    def _start_decryption(self):
        """Start decryption process"""
        if len(self.selected_images) < 2:
            messagebox.showerror("Error", "Please select at least 2 stego images")
            return
            
        master_password = self.decrypt_master_entry.get().strip()
        if not master_password:
            messagebox.showerror("Error", "Please enter master password")
            return
            
        self.decrypt_output.delete("1.0", "end")
        self.decrypt_progress.start_animation()
        self.decrypt_btn.configure(state="disabled")
        self._update_status("Decrypting...", "info")
        
        thread = threading.Thread(
            target=self._decrypt_worker,
            args=(self.selected_images.copy(), master_password)
        )
        thread.daemon = True
        thread.start()
        
    def _decrypt_worker(self, image_paths, master_password):
        """Decryption worker thread"""
        try:
            self._log_output(self.decrypt_output, "Starting decryption process...", "info")
            self._log_output(self.decrypt_output, "━" * 50, "info")
            self._log_output(self.decrypt_output, f"Processing {len(image_paths)} stego images...", "info")
            
            parsed_shares = []
            for i, path in enumerate(image_paths, 1):
                self._log_output(self.decrypt_output, f"Extracting from: {os.path.basename(path)}", "info")
                payload = extract_data_from_image(path)
                meta = self._parse_share_payload(payload)
                parsed_shares.append(meta)
                self._log_output(self.decrypt_output, f"Found share {meta['index']}/{meta['total']}", "success")
                
            if len(parsed_shares) < 2:
                self._log_output(self.decrypt_output, "Not enough valid shares found", "error")
                return
                
            # Validate compatibility
            vs = {s['version'] for s in parsed_shares}
            totals = {s['total'] for s in parsed_shares}
            thresholds = {s['threshold'] for s in parsed_shares}
            pkg_hashes = {s['packaged_cipher'] for s in parsed_shares}
            
            if len(vs) != 1 or len(totals) != 1 or len(thresholds) != 1 or len(pkg_hashes) != 1:
                self._log_output(self.decrypt_output, "Selected shares do not match!", "error")
                return
                
            threshold = parsed_shares[0]['threshold']
            if len(parsed_shares) < threshold:
                self._log_output(self.decrypt_output, f"Need at least {threshold} shares", "error")
                return
                
            self._log_output(self.decrypt_output, "━" * 50, "info")
            self._log_output(self.decrypt_output, "Recovering ephemeral key...", "info")
            
            share_bytes_list = [s['share_bytes'] for s in parsed_shares[:threshold]]
            packaged_cipher = parsed_shares[0]['packaged_cipher']
            
            recovered_k2 = recover_bytes_from_shares(share_bytes_list)
            if len(recovered_k2) < 16:
                recovered_k2 = (b'\x00' * (16 - len(recovered_k2))) + recovered_k2
            elif len(recovered_k2) > 16:
                recovered_k2 = recovered_k2[-16:]
                
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aes = AESGCM(recovered_k2)
            nonce2 = packaged_cipher[:12]
            ct_and_tag = packaged_cipher[12:]
            binary_blob = aes.decrypt(nonce2, ct_and_tag, None)
            
            salt = binary_blob[:16]
            nonce = binary_blob[16:28]
            ciphertext_with_tag = binary_blob[28:]
            
            self._log_output(self.decrypt_output, "Decrypting with master password...", "info")
            plaintext = decrypt_password_aes_gcm(salt, nonce, ciphertext_with_tag, master_password)
            
            self._log_output(self.decrypt_output, "━" * 50, "info")
            self._log_output(self.decrypt_output, "DECRYPTION SUCCESSFUL!", "success")
            self._log_output(self.decrypt_output, "━" * 50, "info")
            self._log_output(self.decrypt_output, f"🔑 Password: {plaintext}", "success")
            self._log_output(self.decrypt_output, f"Length: {len(plaintext)} characters", "info")
            
        except Exception as e:
            self._log_output(self.decrypt_output, f"Decryption failed: {str(e)}", "error")
        finally:
            self.after(0, self._decryption_finished)
            
    def _parse_share_payload(self, payload):
        """Parse wrapped share payload"""
        SHARE_MAGIC = b"FKSS01"
        SHARE_MAGIC_LEN = len(SHARE_MAGIC)
        
        min_header = SHARE_MAGIC_LEN + 1 + 1 + 1 + 1 + 4 + 4
        if len(payload) < min_header:
            raise ValueError("Share payload too short")
        if payload[:SHARE_MAGIC_LEN] != SHARE_MAGIC:
            raise ValueError("Share magic mismatch")
            
        pos = SHARE_MAGIC_LEN
        version = payload[pos]; pos += 1
        index = payload[pos]; pos += 1
        total = payload[pos]; pos += 1
        threshold = payload[pos]; pos += 1
        share_len = int.from_bytes(payload[pos:pos+4], 'big'); pos += 4
        packaged_cipher_len = int.from_bytes(payload[pos:pos+4], 'big'); pos += 4
        
        if pos + share_len + packaged_cipher_len > len(payload):
            raise ValueError("Declared sizes exceed payload size")
            
        share_bytes = payload[pos:pos+share_len]; pos += share_len
        packaged_cipher = payload[pos:pos+packaged_cipher_len]
        
        return {
            "version": version,
            "index": index,
            "total": total,
            "threshold": threshold,
            "share_len": share_len,
            "packaged_cipher_len": packaged_cipher_len,
            "share_bytes": share_bytes,
            "packaged_cipher": packaged_cipher
        }
        
    def _decryption_finished(self):
        """Called when decryption is finished — clear password and selected images."""
        self.decrypt_progress.stop_animation()
        self.decrypt_btn.configure(state="normal")
        self._update_status("Decryption completed", "success")
        self.decrypt_master_entry.delete(0, "end")
        self.selected_images = []
        self._update_image_list()
        
    # ═══════════════════════════════════════════════════════════════════════════
    # MANUAL DECRYPTION LOGIC
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _browse_manual_file(self):
        """Browse for manual decryption file"""
        file_path = native_file_dialog(
            self,
            title="Select .bin file for decryption",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")],
            mode="open",
            initialdir=os.path.expanduser("~/Downloads")
        )
        if file_path:
            self.manual_file_entry.delete(0, "end")
            self.manual_file_entry.insert(0, file_path)
            
    def _start_manual_decryption(self):
        """Start manual decryption"""
        file_path = self.manual_file_entry.get().strip()
        master_password = self.manual_master_entry.get().strip()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a .bin file")
            return
            
        if not master_password:
            messagebox.showerror("Error", "Please enter master password")
            return
            
        self.manual_output.delete("1.0", "end")
        
        try:
            self._log_output(self.manual_output, "Starting manual decryption...", "info")
            self._log_output(self.manual_output, "━" * 50, "info")
            self._log_output(self.manual_output, f"File: {os.path.basename(file_path)}", "info")
            
            with open(file_path, "rb") as f:
                binary_blob = f.read()
                
            self._log_output(self.manual_output, f"File size: {len(binary_blob)} bytes", "info")
                
            if len(binary_blob) < 28:
                self._log_output(self.manual_output, "File too small to be valid", "error")
                return
                
            salt = binary_blob[:16]
            nonce = binary_blob[16:28]
            ciphertext_with_tag = binary_blob[28:]
            
            self._log_output(self.manual_output, "Decrypting with master password...", "info")
            plaintext = decrypt_password_aes_gcm(salt, nonce, ciphertext_with_tag, master_password)
            
            self._log_output(self.manual_output, "━" * 50, "info")
            self._log_output(self.manual_output, "DECRYPTION SUCCESSFUL!", "success")
            self._log_output(self.manual_output, "━" * 50, "info")
            self._log_output(self.manual_output, f"🔑 Password: {plaintext}", "success")
            self._log_output(self.manual_output, f"Length: {len(plaintext)} characters", "info")
            
            self._update_status("Manual decryption completed", "success")
            
        except Exception as e:
            self._log_output(self.manual_output, f"Manual decryption failed: {str(e)}", "error")
            self._update_status("Manual decryption failed", "error")
        finally:
            # Clear file path and password so they are not left visible
            self.manual_file_entry.delete(0, "end")
            self.manual_master_entry.delete(0, "end")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    app = FracturedKeyApp()
    app.mainloop()

if __name__ == "__main__":
    main()
