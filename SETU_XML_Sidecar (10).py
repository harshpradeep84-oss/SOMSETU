import streamlit as st
import numpy as np
import cv2
from PIL import Image, ExifTags, ImageStat
import pandas as pd
import hashlib, io, json, math, os, tempfile, time, re, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

APP_NAME = "SOMSETU"
TEAM_NAME = "Team Tejasnet"
PROJECT_UNIVERSITY = "Veer Bahadur Singh Purvanchal University, Jaunpur"
PROJECT_DEPARTMENT = "Computer Science & Engineering"
PROJECT_CONTACT = "harshpradeep84@gmail.com"
TEAM_CONTACT = ""

st.set_page_config(page_title="SOMSETU | Lunar Image Registration", page_icon="🌙", layout="wide", initial_sidebar_state="collapsed")

st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800&display=swap');
.stApp {background: radial-gradient(circle at 50% 10%, rgba(30,66,100,.13), transparent 34%), linear-gradient(115deg, rgba(0,0,0,.84), rgba(0,0,0,.76) 48%, rgba(0,0,0,.90)), url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=2400&q=85') center/cover fixed; color:#edf4ff;}
[data-testid="stHeader"] {background:rgba(4,9,27,.35)}
[data-testid="stSidebar"] {background:linear-gradient(180deg,rgba(0,0,0,.985),rgba(4,7,15,.97)); border-right:1px solid rgba(126,177,255,.2)}
.block-container {padding-top:1.1rem; padding-bottom:2.5rem; max-width:1240px; margin-left:auto; margin-right:auto}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display:none!important}
section[data-testid="stMain"] {margin-left:0!important}
[data-testid="stFileUploader"] section {padding:1rem!important}
[data-testid="stFileUploader"] {min-height:92px}
.hero {padding:34px 34px; border:1px solid rgba(130,180,255,.28); border-radius:22px; background:linear-gradient(120deg,rgba(0,0,0,.89),rgba(4,8,14,.82)); box-shadow:0 18px 60px rgba(0,0,0,.25); margin-bottom:18px}
.brand {font-family:Orbitron,sans-serif; font-size:48px; letter-spacing:5px; font-weight:800; color:#eaf4ff; text-shadow:0 0 24px rgba(74,177,255,.5)}
.subbrand {font-family:Inter,sans-serif; font-size:12px; letter-spacing:2px; color:#88d8ff; text-transform:uppercase}
.hero p {color:#c3d4f3; margin-bottom:0}
.glass-card {border:1px solid rgba(135,177,255,.24);background:rgba(0,0,0,.78);border-radius:17px;padding:20px;backdrop-filter:blur(10px);height:100%;box-shadow:0 10px 30px rgba(0,0,0,.16)}
.panel {border:1px solid rgba(135,177,255,.22); background:rgba(0,0,0,.80); border-radius:17px; padding:18px 20px; backdrop-filter:blur(8px)}
.metric {background:linear-gradient(135deg,rgba(5,12,22,.94),rgba(0,0,0,.92)); border:1px solid rgba(126,177,255,.22); border-radius:14px; padding:15px 17px; min-height:100px}
.metric-label {font-size:12px; color:#9bb6dd; text-transform:uppercase; letter-spacing:1px}
.metric-value {font-family:Orbitron,sans-serif; font-size:25px; font-weight:700; color:#f3f8ff; margin-top:8px}
.small-note {font-size:12px;color:#a9bddf}
div.stButton>button {border-radius:10px;border:1px solid #58b8f8;background:linear-gradient(90deg,#1478bd,#6a54d9);color:white;font-weight:700;min-height:44px}
div.stDownloadButton>button {border-radius:10px;border:1px solid #55c5ff;background:rgba(20,65,110,.75);color:#fff;font-weight:600}
section[data-testid="stFileUploader"] {border:1px dashed rgba(109,190,255,.45); border-radius:12px; background:rgba(8,19,42,.55); padding:8px}
h1,h2,h3 {color:#f1f6ff!important}
footer {visibility:hidden}
[data-testid='stAppViewContainer'] {background:transparent}
.topnav {border:1px solid rgba(128,180,255,.25);border-radius:15px;background:rgba(0,0,0,.91);padding:8px 14px;margin-bottom:18px}
.center-wrap {max-width:1180px;margin:0 auto}
.stNumberInput input,.stSelectbox div[data-baseweb='select'] {background:rgba(5,10,18,.96)!important}
div[data-testid='stExpander'] {border:1px solid rgba(93,174,255,.25)!important;border-radius:14px!important;background:rgba(0,0,0,.42)!important}
[data-testid='stTabs'] button {font-weight:700}
.team-tag {color:#8ed9ff;font-size:12px;letter-spacing:1.5px;text-align:right;padding-top:14px}
.hero-kicker {color:#8ed9ff;letter-spacing:3px;font-size:12px;font-weight:700}
.stButton button {transition:all .18s ease; box-shadow:0 0 0 rgba(67,174,255,0)}
.stButton button:hover {border-color:#8ee4ff!important;box-shadow:0 0 18px rgba(55,165,255,.22)!important;transform:translateY(-1px)}
[data-testid='stMetric'] {background:rgba(0,0,0,.48);border:1px solid rgba(112,180,255,.22);padding:12px;border-radius:12px}
[data-testid='stImage'] img {border:1px solid rgba(107,182,255,.23);border-radius:10px}
.hero-copy {font-size:17px;color:#c8d9f5;max-width:780px}
/* SOMSETU visual upgrade */
.stApp {background:radial-gradient(circle at 12% 8%,rgba(0,220,255,.20),transparent 28%),radial-gradient(circle at 86% 18%,rgba(168,85,247,.18),transparent 30%),radial-gradient(circle at 55% 92%,rgba(16,185,129,.13),transparent 28%),linear-gradient(120deg,rgba(2,6,23,.92),rgba(8,12,32,.84) 48%,rgba(16,8,30,.92)),url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=2400&q=85') center/cover fixed}
.hero{background:linear-gradient(135deg,rgba(3,12,30,.94),rgba(19,8,45,.86) 48%,rgba(2,35,45,.88));border-color:rgba(99,230,255,.35);box-shadow:0 20px 70px rgba(0,0,0,.42),0 0 35px rgba(56,189,248,.08)}
.glass-card,.panel{background:linear-gradient(135deg,rgba(4,15,31,.90),rgba(17,10,38,.84));border-color:rgba(99,230,255,.24);box-shadow:0 14px 40px rgba(0,0,0,.22)}
.metric{background:linear-gradient(135deg,rgba(6,27,45,.94),rgba(30,12,58,.92));border-color:rgba(103,232,249,.28)}
.brand{text-shadow:0 0 16px rgba(34,211,238,.50),0 0 38px rgba(168,85,247,.24)}
.subbrand,.hero-kicker{color:#67e8f9}
.topnav{background:linear-gradient(90deg,rgba(3,16,32,.94),rgba(30,10,52,.92),rgba(3,28,35,.94));border-color:rgba(103,232,249,.28)}
section[data-testid="stFileUploader"]{background:linear-gradient(135deg,rgba(5,25,43,.72),rgba(35,13,53,.60));border-color:rgba(103,232,249,.48)}
div.stButton>button{background:linear-gradient(90deg,#0891b2,#7c3aed,#db2777);border-color:rgba(103,232,249,.55);box-shadow:0 5px 20px rgba(124,58,237,.22)}
div.stDownloadButton>button{background:linear-gradient(90deg,rgba(8,145,178,.72),rgba(79,70,229,.72));border-color:rgba(103,232,249,.45)}
[data-testid='stTabs'] button[aria-selected='true']{color:#67e8f9!important;border-bottom-color:#a855f7!important}
.xml-badge{display:inline-block;padding:7px 12px;border-radius:999px;background:linear-gradient(90deg,rgba(8,145,178,.22),rgba(124,58,237,.25));border:1px solid rgba(103,232,249,.35);color:#bff7ff;font-size:12px;font-weight:700;letter-spacing:.4px}
.auto-card{padding:16px 18px;border-radius:16px;background:linear-gradient(135deg,rgba(6,78,59,.28),rgba(8,47,73,.30),rgba(76,29,149,.25));border:1px solid rgba(52,211,153,.30);box-shadow:0 10px 30px rgba(0,0,0,.16)}
.info-chip{display:inline-block;margin:4px 5px 4px 0;padding:6px 10px;border-radius:10px;background:rgba(14,116,144,.18);border:1px solid rgba(103,232,249,.20);color:#d7fbff;font-size:12px}
.footer-glow{color:#9cefff}

</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def _xml_norm_key(value):
    value = str(value or "").split("}")[-1]
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _xml_float(value):
    if value is None:
        return None
    m = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", str(value))
    return float(m.group(0)) if m else None


def parse_xml_metadata(uploaded):
    """Parse mission XML sidecar without requiring one rigid XML schema.

    The supplied IIRS examples contain product-level mission metadata,
    nested IIR acquisition metadata, process timings, corner coordinates,
    statistics, spacecraft geometry and solar geometry. We retain every
    flattened XML field and additionally expose the important fields in a
    stable canonical structure for the UI.
    """
    raw = uploaded.getvalue()
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML file: {e}")

    flat = {}
    def walk(elem, parent=""):
        tag = _xml_norm_key(elem.tag)
        path = f"{parent}.{tag}" if parent else tag
        text = (elem.text or "").strip()
        if text:
            flat[path] = text
            flat.setdefault(tag, text)
        for k, v in elem.attrib.items():
            nk = _xml_norm_key(k)
            flat[f"{path}.@{nk}"] = str(v)
            flat.setdefault(nk, str(v))
        for child in elem:
            walk(child, path)
    walk(root)

    def first(*names):
        for name in names:
            key = _xml_norm_key(name)
            if key in flat:
                return flat[key]
        return None

    canonical = {
        "job_id": first("job_id"),
        "dataset": first("level0_dataset", "level0_dir_name"),
        "dop": first("dop"),
        "station_id": first("station_id"),
        "dumping_orbit_number": first("dumping_orbit_number"),
        "imaging_orbit_number": first("imaging_orbit_number"),
        "start_time": first("StartTime"),
        "data_type": first("data_type"),
        "integration_time_ms": first("integration_time_ms"),
        "image_width": first("image_width"),
        "spacecraft_altitude_km": first("spacecraft_altitude_in_km"),
        "resolution_m": first("Resolution_in_meter", "resolution_in_meter"),
        "roll_deg": first("Roll_in_degree"),
        "pitch_deg": first("Pitch_in_degree"),
        "yaw_deg": first("Yaw_in_degree"),
        "sun_azimuth_deg": first("Sun_azimuth_in_degree"),
        "sun_elevation_deg": first("Sun_elevation_in_degree"),
        "solar_incidence_deg": first("Solar_incidence_angle_in_degree"),
        "projection": first("projection"),
        "area": first("area"),
        "orbit_limb_direction": first("orbit_limb_direction"),
        "spacecraft_yaw_direction": first("spacecraft_yaw_direction"),
        "no_of_lcps": first("NoOfLCPs"),
        "reference_used": first("ReferenceUsed"),

        # IIR instrument/acquisition fields
        "iir_start_time_utc": first("start_time_utc"),
        "iir_stop_time_utc": first("stop_time_utc"),
        "date_of_pass": first("date_of_pass"),
        "gain": first("gain"),
        "exposure": first("exposure"),
        "exposure_duration": first("exposure_duration"),
        "detector_temperature_k": first("detector_temperature_kelvin"),
        "ter_mirror_temperature": first("ter_mirror_temperature"),
        "spc_casing_temperature": first("spc_casing_temperature"),
        "dewar_vwt_temperature": first("dewar_vwt_temperature"),
        "data_segment_position": first("data_segment_position"),
        "raw_image_width": first("raw_qube_image_width"),
        "raw_image_height": first("raw_qube_image_height"),
        "radiance_image_width": first("radiance_qube_image_width"),
        "radiance_image_height": first("radiance_qube_image_height"),
        "raw_scan": first("brw_raw_scan"),
        "radiance_scan": first("brw_rad_scan"),
        "raw_min": first("raw_min"),
        "raw_max": first("raw_max"),
        "raw_mean": first("raw_mean"),
        "reconstructible_line_loss_pct": first("reconstructible_line_loss_percentage"),
        "non_reconstructible_line_loss_pct": first("non_reconstructible_line_loss_percentage"),
        "grid_records": first("grid_no_of_records"),
        "grid_max_record_length": first("grid_max_record_length"),
        "grid_file_size": first("grid_file_size"),

        # Statistics
        "stat_min": first("minimum"),
        "stat_max": first("maximum"),
        "stat_mean": first("mean"),
        "stat_std": first("standard_deviation"),
    }

    numeric_keys = [
        k for k in canonical
        if k.endswith(("_km","_m","_ms","_deg","_k","_width","_height","_scan",
                       "_min","_max","_mean","_pct","_records","_length","_size"))
        or k in {"integration_time_ms","exposure_duration","dumping_orbit_number",
                 "imaging_orbit_number","no_of_lcps","raw_min","raw_max","raw_mean",
                 "grid_records","grid_max_record_length","grid_file_size",
                 "stat_min","stat_max","stat_mean","stat_std"}
    ]
    for key in numeric_keys:
        if canonical.get(key) is not None:
            val = _xml_float(canonical[key])
            if val is not None:
                canonical[key] = val

    # The sample XML has four geographic corner pairs. Keep both ordinary
    # lat/lon and *_en coordinates when present.
    corners = {}
    for pos in ("topleft","topright","bottomleft","bottomright"):
        for suffix in ("", "_refined", "_en", "_refined_en"):
            lat = first(f"{pos}_latitude{suffix}")
            lon = first(f"{pos}_longitude{suffix}")
            if lat is not None or lon is not None:
                corners.setdefault(pos, {})[suffix or "standard"] = {
                    "latitude": _xml_float(lat) if lat is not None else None,
                    "longitude": _xml_float(lon) if lon is not None else None
                }
    canonical["corners"] = corners

    # Process timing blocks are preserved by their path. Extract the known
    # processing stages for a clean interface.
    processes = {}
    for stage in ("RadiometricCorrection","SelenoTagging","AutoLCP"):
        prefix = _xml_norm_key(stage)
        vals = {}
        for field in ("StartTime","StopTime","ElapsedTimeInSecs"):
            v = first(field)  # fallback below uses path-specific lookup
            path_key = f"product.process.{prefix}.{_xml_norm_key(field)}"
            if path_key in flat:
                vals[_xml_norm_key(field)] = flat[path_key]
        if vals:
            if "elapsed_time_in_secs" in vals:
                vals["elapsed_time_in_secs"] = _xml_float(vals["elapsed_time_in_secs"])
            processes[stage] = vals
    canonical["processing"] = processes

    canonical.update({
        "root_tag": _xml_norm_key(root.tag),
        "field_count": len(flat),
        "sha256": sha256_bytes(raw),
        "file_name": uploaded.name
    })

    # Compatibility aliases used by the existing registration controls.
    if canonical.get("sun_elevation_deg") is not None:
        canonical["sun_elevation"] = canonical["sun_elevation_deg"]
    if canonical.get("sun_azimuth_deg") is not None:
        canonical["sun_azimuth"] = canonical["sun_azimuth_deg"]
    if canonical.get("resolution_m") is not None:
        canonical["pixel_scale"] = canonical["resolution_m"]

    return {"canonical": canonical, "flat": flat}


def apply_xml_context(xml_meta):
    c = (xml_meta or {}).get("canonical", {})
    ranges = {
        "sun_elevation": (0,90), "sun_azimuth": (0,359),
        "expected_scale": (.01,15), "max_shift": (0,100000),
        "shift_x_context": (-100000,100000), "shift_y_context": (-100000,100000),
        "ratio": (.50,.99), "ransac_px": (.5,20),
        "max_features": (500,30000), "brightness": (.10,2),
        "min_inlier_ratio": (0,100)
    }
    for key,(lo,hi) in ranges.items():
        v = c.get(key)
        if isinstance(v,(int,float)) and lo <= v <= hi:
            st.session_state[key] = v


def xml_coordinate_summary(xml_meta):
    c = (xml_meta or {}).get("canonical", {})
    out = []
    corners = c.get("corners", {})
    if corners:
        vals = []
        for pos in ("topleft","topright","bottomleft","bottomright"):
            item = corners.get(pos, {}).get("standard")
            if item and item.get("latitude") is not None and item.get("longitude") is not None:
                vals.append(f"{pos}: {item['latitude']:.6f}°, {item['longitude']:.6f}°")
        if vals:
            out.append(" | ".join(vals))
    if c.get("resolution_m") is not None:
        out.append(f"Resolution: {c['resolution_m']:.2f} m/pixel")
    return " · ".join(out) if out else "No recognized coordinate fields found; raw XML fields are retained."


def xml_display_value(v):
    if v is None or v == "":
        return "—"
    if isinstance(v, float):
        return f"{v:.6f}".rstrip("0").rstrip(".")
    return str(v)


def render_xml_interface(meta, title):
    """Compact but complete display of the important fields in the supplied XML."""
    if not meta:
        return
    c = meta["canonical"]
    st.markdown(f"#### 🛰️ {title}")
    st.caption(f"{c.get('file_name','XML')} · {c.get('field_count',0)} fields parsed · SHA-256 {c.get('sha256','')[:24]}…")

    a,b,c1,d = st.columns(4)
    a.metric("Station", xml_display_value(c.get("station_id")))
    b.metric("Imaging Orbit", xml_display_value(c.get("imaging_orbit_number")))
    c1.metric("Altitude", f"{xml_display_value(c.get('spacecraft_altitude_km'))} km")
    d.metric("Resolution", f"{xml_display_value(c.get('resolution_m'))} m/pixel")

    with st.expander("☀️ Solar & spacecraft geometry", expanded=True):
        g = st.columns(6)
        g[0].metric("Sun elevation", f"{xml_display_value(c.get('sun_elevation_deg'))}°")
        g[1].metric("Sun azimuth", f"{xml_display_value(c.get('sun_azimuth_deg'))}°")
        g[2].metric("Solar incidence", f"{xml_display_value(c.get('solar_incidence_deg'))}°")
        g[3].metric("Roll", f"{xml_display_value(c.get('roll_deg'))}°")
        g[4].metric("Pitch", f"{xml_display_value(c.get('pitch_deg'))}°")
        g[5].metric("Yaw", f"{xml_display_value(c.get('yaw_deg'))}°")
        st.write(f"**Projection:** {xml_display_value(c.get('projection'))}  ·  **Area:** {xml_display_value(c.get('area'))}  ·  **Limb:** {xml_display_value(c.get('orbit_limb_direction'))}")

    with st.expander("📍 Image / lunar coordinates", expanded=True):
        corner_rows = []
        for pos in ("topleft","topright","bottomleft","bottomright"):
            item = c.get("corners",{}).get(pos,{})
            std = item.get("standard",{})
            refined = item.get("_refined",{})
            en = item.get("_en",{})
            ren = item.get("_refined_en",{})
            corner_rows.append({
                "Corner": pos.replace("_"," ").title(),
                "Latitude": xml_display_value(std.get("latitude")),
                "Longitude": xml_display_value(std.get("longitude")),
                "Refined Lat": xml_display_value(refined.get("latitude")),
                "Refined Lon": xml_display_value(refined.get("longitude")),
                "EN Lat": xml_display_value(en.get("latitude")),
                "EN Lon": xml_display_value(en.get("longitude")),
                "Refined EN Lat": xml_display_value(ren.get("latitude")),
                "Refined EN Lon": xml_display_value(ren.get("longitude"))
            })
        if any(row["Latitude"] != "—" for row in corner_rows):
            st.dataframe(pd.DataFrame(corner_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No corner coordinates were found.")

    with st.expander("🔬 Instrument & acquisition metadata", expanded=False):
        rows = [
            ("Job ID",c.get("job_id")),("Dataset",c.get("dataset")),("DOP",c.get("dop")),
            ("Data type",c.get("data_type")),("Integration time (ms)",c.get("integration_time_ms")),
            ("IIR start UTC",c.get("iir_start_time_utc")),("IIR stop UTC",c.get("iir_stop_time_utc")),
            ("Date of pass",c.get("date_of_pass")),("Gain",c.get("gain")),("Exposure",c.get("exposure")),
            ("Exposure duration",c.get("exposure_duration")),("Detector temperature (K)",c.get("detector_temperature_k")),
            ("Mirror temperature",c.get("ter_mirror_temperature")),("SPC casing temperature",c.get("spc_casing_temperature")),
            ("Dewar VWT temperature",c.get("dewar_vwt_temperature")),("Segment position",c.get("data_segment_position")),
            ("Raw image",f"{xml_display_value(c.get('raw_image_width'))} × {xml_display_value(c.get('raw_image_height'))}"),
            ("Radiance image",f"{xml_display_value(c.get('radiance_image_width'))} × {xml_display_value(c.get('radiance_image_height'))}"),
            ("Raw scan",c.get("raw_scan")),("Radiance scan",c.get("radiance_scan")),
            ("Raw min/max/mean",f"{xml_display_value(c.get('raw_min'))} / {xml_display_value(c.get('raw_max'))} / {xml_display_value(c.get('raw_mean'))}"),
            ("Line loss (reconstructible %)",c.get("reconstructible_line_loss_pct")),
            ("Line loss (non-reconstructible %)",c.get("non_reconstructible_line_loss_pct")),
            ("Grid records",c.get("grid_records")),("Grid max record length",c.get("grid_max_record_length")),
            ("Grid file size",c.get("grid_file_size")),("LCP count",c.get("no_of_lcps")),
            ("Reference used",c.get("reference_used"))
        ]
        st.dataframe(pd.DataFrame([{"Field":k,"Value":xml_display_value(v)} for k,v in rows]),
                     use_container_width=True, hide_index=True)

    with st.expander("⚙️ Processing history", expanded=False):
        proc = c.get("processing",{})
        if proc:
            st.dataframe(pd.DataFrame([
                {"Stage":stage,"Start":vals.get("start_time"),"Stop":vals.get("stop_time"),
                 "Elapsed (s)":vals.get("elapsed_time_in_secs")}
                for stage,vals in proc.items()
            ]), use_container_width=True, hide_index=True)
        else:
            st.info("No processing-stage timing blocks recognized.")

    with st.expander("📊 Image statistics", expanded=False):
        stats = pd.DataFrame([{
            "Minimum": c.get("stat_min"), "Maximum": c.get("stat_max"),
            "Mean": c.get("stat_mean"), "Std. deviation": c.get("stat_std")
        }])
        st.dataframe(stats, use_container_width=True, hide_index=True)

    with st.expander("🧾 Complete parsed XML fields", expanded=False):
        st.dataframe(pd.DataFrame(
            [{"XML field":k,"Value":v} for k,v in meta.get("flat",{}).items()]
        ), use_container_width=True, hide_index=True)

def image_from_upload(uploaded):
    raw = uploaded.getvalue()
    name = uploaded.name.lower()
    if name.endswith(('.mp4','.mov','.avi','.mkv','.webm','.m4v')):
        suffix = os.path.splitext(name)[1] or '.mp4'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(raw); path=f.name
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            cap.release(); os.unlink(path)
            raise ValueError('Video could not be decoded by OpenCV. Try MP4 (H.264) or upload a still image.')
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
        frame_idx = max(0, total//2)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        cap.release(); os.unlink(path)
        if not ok or frame is None:
            raise ValueError('Could not extract a representative frame from this video.')
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb), {'media_type':'Video (representative middle frame)','frame_count':total,'fps':round(fps,3),'selected_frame':frame_idx,'duration_seconds':round(total/fps,3) if fps>0 else None,'raw':raw}
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
        return im.convert('RGB'), {'media_type':f'Image ({im.format or "unknown format"})','raw':raw,'original_format':im.format,'mode':im.mode}
    except Exception as e:
        raise ValueError(f'Unsupported or unreadable image: {e}')

def image_integrity_screen(uploaded, pil_img, info):
    raw = info['raw']; arr = np.asarray(pil_img)
    h,w = arr.shape[:2]
    findings=[]
    score=0
    ext = os.path.splitext(uploaded.name)[1].lower()
    fmt = info.get('original_format','')
    ext_map={'.jpg':'JPEG','.jpeg':'JPEG','.png':'PNG','.tif':'TIFF','.tiff':'TIFF','.bmp':'BMP','.webp':'WEBP'}
    if fmt and ext in ext_map and ext_map[ext] != fmt.upper():
        findings.append('File extension and decoded image format do not match; verify the source file.'); score+=1
    if w < 64 or h < 64:
        findings.append('Very small image dimensions; unsuitable for reliable scientific registration.'); score+=1
    gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
    std=float(np.std(gray)); entropy=float(ImageStat.Stat(pil_img.convert('L')).mean[0])
    if std < 2.0:
        findings.append('Image has very low intensity variation; it may be blank, clipped or unsuitable.'); score+=1
    exif_count=0
    try:
        with Image.open(io.BytesIO(raw)) as exim:
            exif=exim.getexif(); exif_count=len(exif)
    except Exception: pass
    if not exif_count and info.get('media_type','').startswith('Image'):
        findings.append('No EXIF metadata found. This is common in scientific rasters and does not imply manipulation.')
    if not findings:
        findings.append('No obvious file-integrity issue detected by these basic checks.')
    status='Review recommended' if score else 'No obvious issue detected'
    return {'status':status,'findings':findings,'sha256':sha256_bytes(raw),'width':w,'height':h,'channels':3,'file_size_bytes':len(raw),'std_intensity':round(std,3),'mean_gray':round(entropy,3),'exif_field_count':exif_count,'format':fmt or info.get('media_type','unknown'),'heuristic_flags':score}

def to_gray_u8(pil_img, illumination_correction=False):
    arr=np.asarray(pil_img.convert('RGB'))
    gray=cv2.cvtColor(arr,cv2.COLOR_RGB2GRAY)
    if gray.dtype != np.uint8: gray=cv2.normalize(gray,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
    if illumination_correction: gray=cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(gray)
    return gray

class RegistrationFailure(Exception):
    def __init__(self, message, diagnostics=None):
        super().__init__(message)
        self.diagnostics = diagnostics or {}

def _registration_working_gray(pil_img, illumination_correction=False, max_dim=2200, max_pixels=6_000_000):
    """Create a bounded-size working image for feature extraction.
    Full-resolution pixels are kept for the final warp/output; feature extraction
    is intentionally performed on a smaller copy so large satellite strips stay fast.
    """
    gray = to_gray_u8(pil_img, illumination_correction)
    h, w = gray.shape[:2]
    scale = min(1.0, float(max_dim) / max(h, w), math.sqrt(float(max_pixels) / max(1, h*w)))
    if scale < 0.999:
        nw, nh = max(32, int(round(w*scale))), max(32, int(round(h*scale)))
        gray = cv2.resize(gray, (nw, nh), interpolation=cv2.INTER_AREA)
    return gray, float(scale)


def register_images(source_pil, reference_pil, detector_name='SIFT', ratio=0.75, ransac_px=4.0, max_features=8000, model='Homography', illumination_correction=False, fast_mode=False):
    # IMPORTANT PERFORMANCE DESIGN:
    # detect/describe on bounded working copies, but estimate the final transform
    # and produce the registered image in original/full-resolution coordinates.
    src_full = np.asarray(source_pil.convert('RGB'))
    ref_full = np.asarray(reference_pil.convert('RGB'))
    src, src_scale = _registration_working_gray(source_pil, illumination_correction)
    ref, ref_scale = _registration_working_gray(reference_pil, illumination_correction)

    effective_features = int(max(500, min(int(max_features), 6000 if fast_mode else 30000)))
    if detector_name == 'SIFT' and hasattr(cv2,'SIFT_create'):
        detector=cv2.SIFT_create(nfeatures=effective_features, contrastThreshold=0.04)
        norm=cv2.NORM_L2; used='SIFT'
    elif detector_name == 'AKAZE':
        detector=cv2.AKAZE_create(); norm=cv2.NORM_HAMMING; used='AKAZE'
    else:
        detector=cv2.ORB_create(nfeatures=effective_features, scaleFactor=1.2, nlevels=8, fastThreshold=12)
        norm=cv2.NORM_HAMMING; used='ORB'

    kp1,des1=detector.detectAndCompute(src,None)
    kp2,des2=detector.detectAndCompute(ref,None)
    if des1 is None or des2 is None or len(kp1)<4 or len(kp2)<4:
        raise RegistrationFailure('Not enough detectable features.', {
            'stage':'Feature detection','keypoints_source':len(kp1),'keypoints_reference':len(kp2),
            'candidate_matches':0,'inliers':0,
            'suggestion':'Use images with visible texture/overlap, or try another detector.'})

    matcher=cv2.BFMatcher(norm)
    # Compute the expensive KNN descriptor search ONCE. Earlier versions repeated
    # this search for every relaxed ratio, which was a major source of latency.
    pairs=matcher.knnMatch(des1,des2,k=2)
    pair_data=[(m,n) for pair in pairs if len(pair)==2 for m,n in [pair]]
    tried_ratios=[]; good=[]; used_ratio=None
    for rr in sorted(set([float(ratio), 0.70, 0.78, 0.85, 0.90, 0.95])):
        if rr < float(ratio):
            continue
        tried_ratios.append(rr)
        candidate=[m for m,n in pair_data if m.distance < rr*n.distance]
        if len(candidate) >= 4:
            good=candidate; used_ratio=rr; break

    if len(good)<4:
        # Mutual matching uses already-computed descriptor distances only as a
        # fallback; cap it to the strongest 300 pairs for faster RANSAC.
        forward=matcher.match(des1,des2)
        reverse=matcher.match(des2,des1)
        rev_best={m.queryIdx:m.trainIdx for m in reverse}
        mutual=[m for m in forward if rev_best.get(m.trainIdx)==m.queryIdx]
        mutual=sorted(mutual,key=lambda m:m.distance)[:max(4,min(300,len(mutual)))]
        if len(mutual)>=4:
            good=mutual; used_ratio=None
        else:
            raise RegistrationFailure(
                f'Only {len(good)} candidate matches survived adaptive filtering.',
                {'stage':'Feature matching','keypoints_source':len(kp1),'keypoints_reference':len(kp2),
                 'candidate_matches':len(good),'inliers':0,'tried_ratios':tried_ratios,
                 'suggestion':'Try images with more overlapping terrain/texture or another image pair.'})

    # Working-image coordinates -> full-resolution coordinates.
    src_pts_small=np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    ref_pts_small=np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
    src_pts=src_pts_small / max(src_scale, 1e-12)
    ref_pts=ref_pts_small / max(ref_scale, 1e-12)

    if model == 'Affine (partial)':
        M, inlier_mask=cv2.estimateAffinePartial2D(
            src_pts,ref_pts,method=cv2.RANSAC,ransacReprojThreshold=float(ransac_px),
            maxIters=1800,confidence=0.99,refineIters=10)
        if M is None:
            raise RegistrationFailure('Affine transform estimation failed.', {'stage':'Geometric registration','candidate_matches':len(good),'inliers':0,'suggestion':'Try Homography or another image pair.'})
        H=np.vstack([M,[0,0,1]])
    else:
        H, inlier_mask=cv2.findHomography(
            src_pts,ref_pts,cv2.RANSAC,float(ransac_px),maxIters=1800,confidence=0.99)
        if H is None:
            raise RegistrationFailure('Homography estimation failed.', {'stage':'Geometric registration','candidate_matches':len(good),'inliers':0,'suggestion':'Images may not overlap or matches may be unreliable.'})

    mask=inlier_mask.ravel().astype(bool) if inlier_mask is not None else np.zeros(len(good),dtype=bool)
    in_src=src_pts.reshape(-1,2)[mask]; in_ref=ref_pts.reshape(-1,2)[mask]
    if len(in_src):
        projected=cv2.perspectiveTransform(in_src.reshape(-1,1,2),H).reshape(-1,2)
        residual=np.linalg.norm(projected-in_ref,axis=1)
        rmse=float(np.sqrt(np.mean(residual**2)))
        median=float(np.median(residual)); p95=float(np.percentile(residual,95))
    else:
        rmse=median=p95=float('nan')

    rh,rw=ref_full.shape[:2]
    if model == 'Affine (partial)':
        warped=cv2.warpAffine(src_full,H[:2,:],(rw,rh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    else:
        warped=cv2.warpPerspective(src_full,H,(rw,rh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)

    occupied=set()
    for x,y in in_ref:
        gx=min(3,max(0,int(x/max(1,rw)*4))); gy=min(3,max(0,int(y/max(1,rh)*4))); occupied.add((gx,gy))
    coverage=len(occupied)/16.0
    inlier_count=int(mask.sum()); inlier_ratio=inlier_count/max(1,len(good))
    if len(in_src):
        displacement=in_ref-in_src
        shift_x=float(np.median(displacement[:,0])); shift_y=float(np.median(displacement[:,1]))
    else:
        shift_x=shift_y=float('nan')
    estimated_scale=float(np.sqrt(abs(np.linalg.det(H[:2,:2]))))
    ref_rgb=ref_full
    overlay=cv2.addWeighted(warped,0.5,ref_rgb,0.5,0)

    # Draw only on the bounded working copies. This is much faster than drawing
    # thousands of keypoints on the original multi-megapixel products.
    selected=[good[i] for i in np.where(mask)[0]][:200]
    left=cv2.cvtColor(src,cv2.COLOR_GRAY2BGR); right=cv2.cvtColor(ref,cv2.COLOR_GRAY2BGR)
    vis_matches=cv2.drawMatches(left,kp1,right,kp2,selected,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    residual_score = 0.0 if not np.isfinite(rmse) else max(0.0, min(1.0, 1.0-rmse/10.0))
    count_score = min(1.0, inlier_count/60.0)
    confidence_score = float(max(0.0, min(100.0, 100.0*(0.38*inlier_ratio + 0.22*count_score + 0.22*coverage + 0.18*residual_score))))
    if inlier_count < 4 or inlier_ratio < 0.15: quality='Low'
    elif confidence_score >= 75 and inlier_ratio >= 0.50 and coverage >= 0.45: quality='Strong geometric fit'
    elif confidence_score >= 55 and inlier_ratio >= 0.30 and coverage >= 0.25: quality='Promising'
    else: quality='Review required'
    match_status = 'Successfully matched' if confidence_score >= 70 and inlier_count >= 10 and inlier_ratio >= 0.35 and coverage >= 0.25 else 'Matched with review'
    points=pd.DataFrame({
        'source_x_px':in_src[:,0] if len(in_src) else [],
        'source_y_px':in_src[:,1] if len(in_src) else [],
        'reference_x_px':in_ref[:,0] if len(in_ref) else [],
        'reference_y_px':in_ref[:,1] if len(in_ref) else [],
        'reprojection_error_px':residual if len(in_src) else []})
    return {
        'warped':warped,'overlay':overlay,'matches_vis':vis_matches[:,:,::-1],'H':H,'detector':used,'model':model,
        'keypoints_source':len(kp1),'keypoints_reference':len(kp2),'candidate_matches':len(good),
        'matching_ratio_used':used_ratio if used_ratio is not None else float(ratio),
        'inlier_count':inlier_count,'inlier_ratio':inlier_ratio,'shift_x_px':shift_x,'shift_y_px':shift_y,
        'estimated_scale':estimated_scale,'rmse':rmse,'median_error':median,'p95_error':p95,'coverage':coverage,
        'quality':quality,'confidence_score':confidence_score,'match_percentage':inlier_ratio*100.0,
        'match_status':match_status,'points':points,'source_shape':src_full.shape,'reference_shape':ref_full.shape,
        'working_scale_source':src_scale,'working_scale_reference':ref_scale}


def register_images_auto(source_pil, reference_pil, illumination_correction=True):
    """Fast automatic registration.
    One strong SIFT pass is attempted first; fallback detectors are only run when
    the first result is weak. This avoids the old six-pass full-resolution cost.
    """
    attempts = [
        ('SIFT', 0.80, 5.0, 6000, 'Homography'),
        ('ORB', 0.85, 6.0, 5000, 'Homography'),
        ('AKAZE', 0.82, 6.0, 5000, 'Homography'),
        ('SIFT', 0.82, 7.0, 6000, 'Affine (partial)'),
    ]
    results=[]; errors=[]
    for detector,ratio,ransac,max_features,model in attempts:
        try:
            r=register_images(source_pil,reference_pil,detector,ratio,ransac,max_features,model,illumination_correction,fast_mode=True)
            rmse=r['rmse'] if np.isfinite(r['rmse']) else 999.0
            score=(min(r['inlier_count'],120)/120)*0.32 + r['inlier_ratio']*0.32 + r['coverage']*0.22 + max(0.0,1.0-rmse/10.0)*0.14
            r['auto_score']=float(score)
            r['auto_attempt']=f'{detector} / {model} / ratio {ratio:.2f} / RANSAC {ransac:.1f}px'
            results.append(r)
            # Stop early once the first result is already geometrically strong.
            if r['inlier_count'] >= 15 and r['inlier_ratio'] >= 0.35 and r['coverage'] >= 0.25 and r['confidence_score'] >= 65:
                break
        except Exception as e:
            diag=getattr(e,'diagnostics',{}) or {}
            errors.append({
                'attempt':f'{detector}/{model}/ratio {ratio:.2f}/RANSAC {ransac:.1f}px',
                'error':str(e),'stage':diag.get('stage','Registration'),
                'keypoints_source':diag.get('keypoints_source'),'keypoints_reference':diag.get('keypoints_reference'),
                'candidate_matches':diag.get('candidate_matches',0),'inliers':diag.get('inliers',0)})
    if not results:
        raise RegistrationFailure('Automatic registration could not find a stable geometric solution.', {
            'stage':'Registration','attempts':errors,
            'suggestion':'Check image overlap, texture, scale and mission pairing. Fast automatic recovery exhausted its strategies.'})
    best=max(results,key=lambda x:x.get('auto_score',-1))
    best['auto_candidates_tested']=len(results); best['auto_failures']=errors
    best['quality'] = 'Strong geometric fit' if best['auto_score']>=0.72 else ('Promising' if best['auto_score']>=0.50 else 'Low')
    return best

def png_bytes(arr):
    im=Image.fromarray(np.uint8(np.clip(arr,0,255)))
    b=io.BytesIO(); im.save(b,format='PNG'); return b.getvalue()

def make_pdf(report, metrics, source_name, ref_name, output_png, points_csv):
    buff=io.BytesIO(); doc=SimpleDocTemplate(buff,pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=15*mm,bottomMargin=15*mm)
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='SETUTitle',parent=styles['Title'],textColor=colors.HexColor('#173e70'),fontSize=23,leading=28,spaceAfter=4)); styles.add(ParagraphStyle(name='Sub',parent=styles['Normal'],textColor=colors.HexColor('#48617c'),fontSize=9,leading=13))
    story=[Paragraph('SETU — Lunar Image Registration Report',styles['SETUTitle']),Paragraph('Space-image Estimation, Tracking &amp; Unification | Team Tejasnet',styles['Sub']),Spacer(1,8),Paragraph('Run timestamp (UTC): '+report['timestamp_utc'],styles['Normal']),Paragraph('Source: '+source_name+'<br/>Reference: '+ref_name,styles['Normal']),Spacer(1,10)]
    rows=[['Metric','Result'],['MATCH STATUS',metrics.get('match_status','Matched with review')],['REGISTRATION CONFIDENCE',f"{metrics.get('confidence_score',0):.1f}%"],['MATCHED / ACCEPTED RATIO',f"{metrics.get('match_percentage',metrics.get('inlier_ratio',0)*100):.1f}%"],['Detector / model',metrics['detector']+' / '+metrics['model']],['Source / reference keypoints',f"{metrics['keypoints_source']} / {metrics['keypoints_reference']}"],['Candidate matches',str(metrics['candidate_matches'])],['RANSAC inliers',str(metrics['inlier_count'])],['Inlier ratio',f"{metrics['inlier_ratio']:.3f}"],['Inlier reprojection RMSE (px)',f"{metrics['rmse']:.4f}" if np.isfinite(metrics['rmse']) else 'N/A'],['Median reprojection error (px)',f"{metrics['median_error']:.4f}" if np.isfinite(metrics['median_error']) else 'N/A'],['95th percentile error (px)',f"{metrics['p95_error']:.4f}" if np.isfinite(metrics['p95_error']) else 'N/A'],['4x4 reference grid coverage',f"{metrics['coverage']*100:.1f}%"],['Heuristic fit label',metrics['quality']]]
    tab=Table(rows,colWidths=[78*mm,85*mm],repeatRows=1); tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#173e70')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c5d2e2')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f2f6fb')]),('VALIGN',(0,0),(-1,-1),'TOP'),('FONTSIZE',(0,0),(-1,-1),8),('PADDING',(0,0),(-1,-1),6)])); story += [tab,Spacer(1,10),Paragraph('Registered product (source warped into reference coordinates)',styles['Heading2'])]
    try:
        im=RLImage(io.BytesIO(output_png),width=165*mm,height=95*mm,kind='proportional'); story.append(im)
    except Exception: pass
    story += [Spacer(1,8),Paragraph('Interpretation and limitations',styles['Heading2']),Paragraph('The confidence score is a transparent registration-quality indicator derived from inlier ratio, inlier count, spatial coverage and reprojection residual. It is NOT a calibrated probability that the two images are identical. The matched/accepted percentage is the share of candidate correspondences retained as RANSAC inliers.',styles['Normal']),Spacer(1,6),Paragraph('RMSE reported here is the residual error of the same RANSAC inlier correspondences used to estimate the transform. It is not an independent ground-truth accuracy measurement and must not be presented as proof of sub-pixel absolute accuracy. Grid coverage measures distribution of inlier points over a 4×4 reference-image grid.',styles['Normal']),Spacer(1,6),Paragraph('Authenticity note: automated file checks cannot prove that an image/video is genuine or unaltered. Use trusted mission provenance, original scientific metadata, checksums and independent review for authenticity decisions.',styles['Normal']),Spacer(1,8),Paragraph('Estimated transform matrix (source → reference)',styles['Heading2']),Paragraph('<font name="Courier">'+json.dumps(report['transform_matrix'])+'</font>',styles['Code']),Spacer(1,8),Paragraph('Generated by SOMSETU prototype. Validate on mission-approved test pairs before operational use.',styles['Sub'])]
    doc.build(story); return buff.getvalue()

# ---------- Main navigation and persistent operator settings ----------
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
nav1, nav2, nav3, nav4, nav5, nav6, nav7, nav8 = st.columns([2.05, 0.62, 0.62, 1.00, 0.72, 0.92, 0.80, 1.12], gap='small')
with nav1:
    st.markdown('<div class="topnav"><span class="brand" style="font-size:27px;letter-spacing:3px">◉ SOMSETU</span><br><span class="subbrand">LUNAR IMAGE CORRESPONDENCE &amp; REGISTRATION</span></div>', unsafe_allow_html=True)
with nav2:
    if st.button('Home', use_container_width=True, key='nav_home'): st.session_state.page='Home'; st.rerun()
with nav3:
    if st.button('About', use_container_width=True, key='nav_about'): st.session_state.page='About & Limitations'; st.rerun()
with nav4:
    if st.button('Registration', use_container_width=True, key='nav_registration'): st.session_state.page='Registration Lab'; st.rerun()
with nav5:
    if st.button('Results', use_container_width=True, key='nav_results'): st.session_state.page='Output Dashboard'; st.rerun()
with nav6:
    if st.button('Integrity', use_container_width=True, key='nav_integrity'): st.session_state.page='Integrity Screening'; st.rerun()
with nav7:
    if st.button('Contact', use_container_width=True, key='nav_contact'): st.session_state.page='Contact'; st.rerun()
with nav8:
    st.markdown('<div class="team-tag">TEAM TEJASNET</div>', unsafe_allow_html=True)
page = st.session_state.page

# Persistent defaults; all operator controls are rendered in the central Registration Lab.
_defaults = {'detector':'SIFT','model':'Homography','ratio':0.75,'ransac_px':4.0,'max_features':8000,
             'sun_elevation':30,'sun_azimuth':120,'illumination_correction':True,'brightness':1.0,
             'expected_scale':1.0,'max_shift':500,'shift_x_context':0,'shift_y_context':0,'min_inlier_ratio':30,'registration_mode':'Automatic'}
if 'source_xml_meta' not in st.session_state: st.session_state.source_xml_meta=None
if 'ref_xml_meta' not in st.session_state: st.session_state.ref_xml_meta=None
for _key,_value in _defaults.items():
    if _key not in st.session_state: st.session_state[_key]=_value

def get_setting(key):
    return st.session_state.get(key, _defaults.get(key))

if page == 'Home':
    st.markdown('<div class="hero"><div class="hero-kicker">LUNAR IMAGE INTELLIGENCE · AUTOMATED RESEARCH WORKSPACE</div><div class="brand">SOMSETU</div><h2 style="margin:0;color:#e7f2ff!important">Space-image Estimation, Tracking &amp; Unification</h2><p class="hero-copy">SOMSETU connects a lunar source image with a reference image and uses their mission XML metadata to understand where, when and under what viewing conditions the image was captured—then automatically estimates the best geometric correspondence.</p><p style="margin-top:16px;font-size:12px;color:#8ff7ff">IMAGE + XML → AUTOMATIC METADATA → ROBUST REGISTRATION → SCIENTIFIC OUTPUT</p></div>',unsafe_allow_html=True)
    hero_a, hero_b = st.columns([1.15,0.85], gap='large')
    with hero_a:
        st.markdown('<div class="glass-card"><h3>🌙 What is SOMSETU?</h3><p>SOMSETU is a research prototype for lunar-image correspondence and registration. Instead of forcing the operator to understand technical solar angles, spacecraft geometry and matching parameters, the system reads the mission XML and presents the useful information in a simple interface.</p><p style="margin-top:12px;color:#8ff7ff"><b>Simple workflow:</b> upload Source Image + Source XML → Reference Image + Reference XML → Run.</p></div>',unsafe_allow_html=True)
        if st.button('🚀 START SOMSETU', use_container_width=True, type='primary', key='start_registration'):
            st.session_state.page='Registration Lab'; st.rerun()
    with hero_b:
        st.markdown('<div class="auto-card"><h3>⚡ Automatic by design</h3><p>Mission metadata is imported from XML. The registration engine automatically tries robust feature-matching strategies and selects the strongest geometrically consistent result.</p><span class="info-chip">☀️ Solar geometry</span><span class="info-chip">📍 Coordinates</span><span class="info-chip">🛰️ Spacecraft pose</span><span class="info-chip">📐 Resolution</span><span class="info-chip">🔬 IIR metadata</span></div>',unsafe_allow_html=True)
    st.markdown('### Why SOMSETU?')
    f1,f2,f3,f4=st.columns(4)
    for col,icon,title,desc in [(f1,'🛰️','Mission-aware','Uses the XML that already travels with the scientific image.'),(f2,'⚡','Automatic','Runs advanced matching automatically, while Manual / Advanced mode remains available.'),(f3,'🗺️','Coordinate-aware','Shows corners, resolution, projection and solar geometry clearly.'),(f4,'📊','Evidence-led','Exports correspondence points, metrics, metadata and reports.')]:
        with col: st.markdown(f'<div class="glass-card"><div style="font-size:27px">{icon}</div><h4>{title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="team-tag" style="text-align:center">BUILT FOR RESEARCH · TEAM TEJASNET</div>',unsafe_allow_html=True)
    st.stop()
elif page == 'Contact':
    st.markdown('<div class="hero"><div class="hero-kicker">CONTACT</div><div class="brand" style="font-size:38px">Contact SOMSETU</div><p>For project-related communication.</p></div>',unsafe_allow_html=True)
    st.markdown(f"""<div class="glass-card" style="max-width:850px;margin:20px auto;">
        <h3>📧 Contact Information</h3>
        <p><b>Email</b><br>{PROJECT_CONTACT}</p>
        <p><b>University / College</b><br>{PROJECT_UNIVERSITY}</p>
        <p><b>Department</b><br>{PROJECT_DEPARTMENT}</p>
    </div>""",unsafe_allow_html=True)
    if st.button('← Back to Home', use_container_width=True):
        st.session_state.page='Home'; st.rerun()
    st.stop()

if 'registration' not in st.session_state: st.session_state.registration=None
if 'source_info' not in st.session_state: st.session_state.source_info=None
if 'ref_info' not in st.session_state: st.session_state.ref_info=None

if page=='Mission Dashboard':
    st.markdown('### Mission dashboard')
    c1,c2,c3,c4=st.columns(4)
    for col,label,value in [(c1,'PIPELINE','READY'),(c2,'REGISTRATION','ON DEMAND'),(c3,'AUTHENTICITY','EVIDENCE-BASED'),(c4,'TEAM','TEJASNET')]:
        col.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value" style="font-size:18px">{value}</div></div>',unsafe_allow_html=True)
    st.write('')
    left,right=st.columns([1.15,0.85],gap='large')
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        st.markdown('#### Mission workflow')
        st.markdown('''1. **Ingest** a source image and a fixed reference image. TIFF/PNG/JPEG are supported; common video formats can be screened and a middle frame extracted.
2. **Screen** basic file integrity, dimensions, metadata presence and SHA-256 checksum.
3. **Correspond** using SIFT, AKAZE or ORB features and descriptor filtering.
4. **Register** with RANSAC-estimated homography or partial affine transform.
5. **Evaluate** inlier count/ratio, reprojection residuals and spatial coverage.
6. **Export** registered image, match-point CSV and a detailed PDF report.''')
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        st.markdown('#### Scientific guardrails')
        st.markdown('''- No fabricated scores or simulated registration outputs.
- RMSE is clearly labeled as an inlier reprojection residual.
- Authenticity screening is **not** a deepfake detector.
- Failed or weak matches are reported as failed/low-confidence, not hidden.
- Validate on mission-provided ground-truth pairs before operational use.''')
        st.markdown('</div>',unsafe_allow_html=True)
    st.info('Start in **Registration Lab** to upload the source and reference images. For best results, use real lunar images with overlapping terrain and retain the original files and provenance.')

elif page=='Registration Lab':
    st.markdown('<div class="hero"><div class="hero-kicker">MISSION WORKSPACE / 01</div><h2>Image Registration Lab</h2><p>Configure image correspondence, illumination handling and geometric estimation. Source is the moving image; reference is the fixed coordinate frame.</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="center-wrap">', unsafe_allow_html=True)
    st.markdown('#### INPUT WORKSPACE · all controls are centered')
    up_a, up_b = st.columns(2, gap='large')
    with up_a:
        st.markdown('<div class="panel"><div class="subbrand">01 / SOURCE IMAGE · MOVING</div><p class="small-note">Chandrayaan-2 OHRC / TMC-2 / IIRS or other lunar raster</p></div>', unsafe_allow_html=True)
        source_file=st.file_uploader('Choose Source Image',type=['png','jpg','jpeg','tif','tiff','bmp','webp','mp4','mov','avi','mkv','webm'],key='source_upload')
    with up_b:
        st.markdown('<div class="panel"><div class="subbrand">02 / REFERENCE IMAGE · FIXED</div><p class="small-note">LRO NAC / WAC, SELENE TC or another overlapping reference</p></div>', unsafe_allow_html=True)
        ref_file=st.file_uploader('Choose Reference Image',type=['png','jpg','jpeg','tif','tiff','bmp','webp','mp4','mov','avi','mkv','webm'],key='ref_upload')

    st.markdown('#### 🧾 MISSION METADATA · JUST UPLOAD XML')
    st.caption('No manual Sun angle, coordinate, scale or shift entry is required. SOMSETU reads the mission sidecar and keeps advanced matching settings automatic.')
    xml_a, xml_b = st.columns(2, gap='large')
    with xml_a:
        source_xml=st.file_uploader('Source Image XML', type=['xml'], key='source_xml_upload')
    with xml_b:
        ref_xml=st.file_uploader('Reference Image XML', type=['xml'], key='ref_xml_upload')

    if source_xml:
        try:
            st.session_state.source_xml_meta=parse_xml_metadata(source_xml)
            apply_xml_context(st.session_state.source_xml_meta)
        except Exception as e:
            st.error(f'Source XML error: {e}')
    if ref_xml:
        try:
            st.session_state.ref_xml_meta=parse_xml_metadata(ref_xml)
            # Reference XML is retained for comparison; source XML seeds operator context first.
        except Exception as e:
            st.error(f'Reference XML error: {e}')

    if source_xml or ref_xml:
        xm1, xm2=st.columns(2, gap='large')
        for col,title,meta in [(xm1,'SOURCE MISSION DATA',st.session_state.get('source_xml_meta')),
                               (xm2,'REFERENCE MISSION DATA',st.session_state.get('ref_xml_meta'))]:
            if meta:
                c=meta['canonical']
                with col:
                    st.markdown(f'<div class="auto-card"><div class="xml-badge">✓ XML READ AUTOMATICALLY</div><h4>{title}</h4><p><b>Product:</b> {xml_display_value(c.get("job_id"))}</p><p><b>Orbit:</b> {xml_display_value(c.get("imaging_orbit_number"))} &nbsp; <b>Station:</b> {xml_display_value(c.get("station_id"))}</p><p><b>Resolution:</b> {xml_display_value(c.get("resolution_m"))} m/pixel &nbsp; <b>Altitude:</b> {xml_display_value(c.get("spacecraft_altitude_km"))} km</p><p><b>Sun:</b> elevation {xml_display_value(c.get("sun_elevation_deg"))}° · azimuth {xml_display_value(c.get("sun_azimuth_deg"))}°</p><p><b>Projection:</b> {xml_display_value(c.get("projection"))} · <b>Area:</b> {xml_display_value(c.get("area"))}</p></div>',unsafe_allow_html=True)
                    st.caption(xml_coordinate_summary(meta))

    # Registration mode: automatic for normal use, manual for operators who want full control.
    st.markdown('### ⚙️ REGISTRATION CONTROL CENTER')
    mode_col1, mode_col2 = st.columns([0.72, 0.28])
    with mode_col1:
        st.radio(
            'Processing mode',
            ['Automatic', 'Manual / Advanced'],
            horizontal=True,
            key='registration_mode',
            help='Automatic lets SOMSETU test robust configurations internally. Manual / Advanced exposes every operator parameter so you can override them when required.'
        )
    with mode_col2:
        if st.session_state.get('registration_mode','Automatic') == 'Automatic':
            st.markdown('<div class="auto-card" style="padding:11px 14px"><b>⚡ AUTO ENGINE</b><br><span class="small-note">XML + adaptive registration</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="auto-card" style="padding:11px 14px"><b>🛠 MANUAL ENGINE</b><br><span class="small-note">Full operator control</span></div>', unsafe_allow_html=True)

    # XML values can seed the manual controls, but they never remove the controls.
    detector=get_setting('detector'); model=get_setting('model'); ratio=get_setting('ratio'); ransac_px=get_setting('ransac_px'); max_features=get_setting('max_features')
    sun_elevation=get_setting('sun_elevation'); sun_azimuth=get_setting('sun_azimuth'); illumination_correction=get_setting('illumination_correction')
    brightness=get_setting('brightness'); expected_scale=get_setting('expected_scale'); max_shift=get_setting('max_shift')
    shift_x_context=get_setting('shift_x_context'); shift_y_context=get_setting('shift_y_context'); min_inlier_ratio=get_setting('min_inlier_ratio')

    with st.expander('🛠️ Manual / Advanced Parameters — all controls', expanded=(st.session_state.get('registration_mode','Automatic') == 'Manual / Advanced')):
        st.caption('These controls are intentionally available for expert/manual operation. XML metadata is still shown above and can pre-fill the mission-context fields.')
        p1,p2,p3,p4 = st.columns(4, gap='medium')
        with p1:
            st.selectbox('Feature detector', ['SIFT','AKAZE','ORB'], key='detector')
            st.selectbox('Geometric model', ['Homography','Affine (partial)'], key='model')
            st.number_input('Max features', min_value=500, max_value=30000, step=500, key='max_features')
        with p2:
            st.number_input('Descriptor ratio threshold', min_value=0.50, max_value=0.99, step=0.01, format='%.2f', key='ratio', help='Lower values are stricter.')
            st.number_input('RANSAC reprojection threshold (px)', min_value=0.5, max_value=20.0, step=0.5, format='%.1f', key='ransac_px')
            st.number_input('Minimum inlier ratio for review (%)', min_value=0, max_value=100, step=5, key='min_inlier_ratio')
        with p3:
            st.number_input('Sun elevation (°)', min_value=0.0, max_value=90.0, step=0.1, format='%.4f', key='sun_elevation')
            st.number_input('Sun azimuth (°)', min_value=0.0, max_value=359.999, step=0.1, format='%.4f', key='sun_azimuth')
            st.checkbox('CLAHE illumination normalization', key='illumination_correction')
        with p4:
            st.number_input('Expected source/reference scale ratio (×)', min_value=0.01, max_value=15.0, step=0.01, format='%.4f', key='expected_scale')
            st.number_input('Expected shift context (px)', min_value=0, max_value=100000, step=25, key='max_shift')
            st.number_input('Expected X shift (px)', min_value=-100000, max_value=100000, step=1, key='shift_x_context')
            st.number_input('Expected Y shift (px)', min_value=-100000, max_value=100000, step=1, key='shift_y_context')
        st.number_input('Display light-glow / brightness factor', min_value=0.10, max_value=2.00, step=0.05, format='%.2f', key='brightness')
        st.info('Manual parameters affect registration only where applicable. Sun/scale/shift values are mission/operator context; the geometric transform is estimated from image correspondences.')

    # Read the final values after widgets/XML have populated session state.
    detector=get_setting('detector'); model=get_setting('model'); ratio=get_setting('ratio'); ransac_px=get_setting('ransac_px'); max_features=get_setting('max_features')
    sun_elevation=get_setting('sun_elevation'); sun_azimuth=get_setting('sun_azimuth'); illumination_correction=get_setting('illumination_correction')
    brightness=get_setting('brightness'); expected_scale=get_setting('expected_scale'); max_shift=get_setting('max_shift')
    shift_x_context=get_setting('shift_x_context'); shift_y_context=get_setting('shift_y_context'); min_inlier_ratio=get_setting('min_inlier_ratio')

    a,b=up_a,up_b
    src_img=ref_img=None; src_integrity=ref_integrity=None
    if source_file:
        try:
            src_img,src_info=image_from_upload(source_file); src_integrity=image_integrity_screen(source_file,src_img,src_info); st.session_state.source_info={'name':source_file.name,'integrity':src_integrity,'info':{k:v for k,v in src_info.items() if k!='raw'}}
            with a:
                st.image(src_img,caption=f"Source preview · {src_img.width} × {src_img.height}",use_container_width=True)
                st.caption(f"SHA-256: {src_integrity['sha256'][:24]}… | {src_integrity['status']}")
        except Exception as e: st.error(f'Source file error: {e}')
    if ref_file:
        try:
            ref_img,ref_info=image_from_upload(ref_file); ref_integrity=image_integrity_screen(ref_file,ref_img,ref_info); st.session_state.ref_info={'name':ref_file.name,'integrity':ref_integrity,'info':{k:v for k,v in ref_info.items() if k!='raw'}}
            with b:
                st.image(ref_img,caption=f"Reference preview · {ref_img.width} × {ref_img.height}",use_container_width=True)
                st.caption(f"SHA-256: {ref_integrity['sha256'][:24]}… | {ref_integrity['status']}")
        except Exception as e: st.error(f'Reference file error: {e}')
    if source_file and ref_file and src_img is not None and ref_img is not None:
        st.markdown('---')
        if src_img.size[0]*src_img.size[1] > 50_000_000 or ref_img.size[0]*ref_img.size[1] > 50_000_000:
            st.warning('One image exceeds 50 megapixels. Processing may use substantial RAM; consider a crop or lower-resolution working copy.')
        if st.button('✦ RUN CORRESPONDENCE & REGISTRATION',use_container_width=True):
            try:
                with st.spinner('Detecting features, matching correspondences and estimating geometric transform…'):
                    if st.session_state.get('registration_mode','Automatic') == 'Manual / Advanced':
                        result=register_images(src_img,ref_img,detector,ratio,ransac_px,max_features,model,illumination_correction,fast_mode=False)
                        result['auto_attempt']=f'MANUAL · {detector} / {model} / ratio {ratio:.2f} / RANSAC {ransac_px:.1f}px'
                        result['auto_candidates_tested']=1
                    else:
                        result=register_images_auto(src_img,ref_img,illumination_correction=True)
                    if brightness != 1.0:
                        result['warped']=np.clip(result['warped'].astype(np.float32)*brightness,0,255).astype(np.uint8)
                        result['overlay']=np.clip(result['overlay'].astype(np.float32)*brightness,0,255).astype(np.uint8)
                    result['source_name']=source_file.name; result['reference_name']=ref_file.name; result['timestamp_utc']=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                    result['source_xml_metadata']=st.session_state.get('source_xml_meta')
                    result['reference_xml_metadata']=st.session_state.get('ref_xml_meta')
                    result['registration_mode']=st.session_state.get('registration_mode','Automatic')
                    result['manual_operator_context']={'detector':detector,'model':model,'ratio':ratio,'ransac_px':ransac_px,'max_features':max_features,'sun_elevation_deg':sun_elevation,'sun_azimuth_deg':sun_azimuth,'illumination_correction':illumination_correction,'brightness':brightness,'expected_scale_ratio':expected_scale,'expected_shift_context_px':max_shift,'expected_shift_x_px':shift_x_context,'expected_shift_y_px':shift_y_context,'minimum_inlier_ratio_for_review_percent':min_inlier_ratio}
                    st.session_state.registration=result
                    st.session_state.registration_diagnostics=None
                    st.session_state.page='Output Dashboard'
                    st.rerun()
            except RegistrationFailure as e:
                st.session_state.registration=None
                st.session_state.registration_diagnostics=e.diagnostics or {'stage':'Registration','error':str(e)}
                st.error(f'Registration did not complete: {e}')
            except Exception as e:
                st.session_state.registration=None
                st.session_state.registration_diagnostics={'stage':'Unexpected error','error':str(e),'suggestion':'Review the uploaded files and try again.'}
                st.error(f'Registration did not complete: {e}')
        result=st.session_state.registration
        diagnostics=st.session_state.get('registration_diagnostics')
        if diagnostics and (not result or result.get('source_name')!=source_file.name or result.get('reference_name')!=ref_file.name):
            st.markdown('### 🔎 Registration diagnostics')
            dcols=st.columns(4)
            diag_attempts=diagnostics.get('attempts',[]) if isinstance(diagnostics,dict) else []
            diag_candidates=max([int(x.get('candidate_matches') or 0) for x in diag_attempts] or [int(diagnostics.get('candidate_matches',0) if isinstance(diagnostics,dict) else 0)])
            diag_inliers=max([int(x.get('inliers') or 0) for x in diag_attempts] or [int(diagnostics.get('inliers',0) if isinstance(diagnostics,dict) else 0)])
            dcols[0].metric('Failure stage',diagnostics.get('stage','Registration'))
            dcols[1].metric('Attempts tested',len(diag_attempts))
            dcols[2].metric('Best candidate matches',diag_candidates)
            dcols[3].metric('Best inliers',diag_inliers)
            if diag_attempts: st.dataframe(pd.DataFrame(diag_attempts),use_container_width=True,hide_index=True)
            st.info('💡 '+str(diagnostics.get('suggestion','Try another detector, increase overlap/texture, or verify the source/reference pairing.')))
        if result and result.get('source_name')==source_file.name and result.get('reference_name')==ref_file.name:
            st.success('Registration completed. Open the separate Output Dashboard to inspect maps, metrics and downloads.')
            if st.button('OPEN OUTPUT DASHBOARD →',use_container_width=True,type='primary'):
                st.session_state.page='Output Dashboard'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif page=='Output Dashboard':
    st.markdown('<div class="hero"><div class="hero-kicker">MISSION WORKSPACE / 02</div><h2>Registration Output Dashboard</h2><p>Source, reference, registered product, correspondence map and measured metrics from the selected run.</p></div>',unsafe_allow_html=True)
    result=st.session_state.get('registration')
    if not result:
        st.info('No registration result is available yet. Open Registration Lab, upload a source and reference image, and run correspondence first.')
        if st.button('GO TO REGISTRATION LAB',type='primary'):
            st.session_state.page='Registration Lab'; st.rerun()
    else:
        src_file_name=result.get('source_name','Source image')
        ref_file_name=result.get('reference_name','Reference image')
        if result.get('match_status')=='Successfully matched':
            st.success(f"✅ {result.get('match_status')} · Registration confidence: {result.get('confidence_score',0):.1f}%")
        else:
            st.warning(f"⚠️ {result.get('match_status','Matched with review')} · Registration confidence: {result.get('confidence_score',0):.1f}%")
        st.caption('Confidence is a registration-quality score, not a probability that the images are identical.')
        if result.get('auto_attempt'):
            st.markdown(f'<div class="auto-card"><b>⚡ Automatic engine selected:</b> {result.get("auto_attempt")} &nbsp; · &nbsp; <b>Configurations tested:</b> {result.get("auto_candidates_tested",1)}</div>',unsafe_allow_html=True)
        c1,c2,c3,c4,c5,c6=st.columns(6)
        for col,label,value in [
            (c1,'MATCH STATUS',result.get('match_status','Matched with review')) ,
            (c2,'CONFIDENCE',f"{result.get('confidence_score',0):.1f}%"),
            (c3,'MATCHED %',f"{result.get('match_percentage',result['inlier_ratio']*100):.1f}%"),
            (c4,'RANSAC INLIERS',result['inlier_count']),
            (c5,'INLIER RMSE',f"{result['rmse']:.3f} px" if np.isfinite(result['rmse']) else 'N/A'),
            (c6,'SPATIAL COVERAGE',f"{result['coverage']*100:.1f}%")]:
            col.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value" style="font-size:20px">{value}</div></div>',unsafe_allow_html=True)
        st.caption(f"Fit assessment: {result['quality']} · {result['detector']} · {result['model']} · {src_file_name} → {ref_file_name}")
        if result['inlier_ratio']*100 < get_setting('min_inlier_ratio'):
            st.warning(f"Inlier ratio is below your review threshold ({get_setting('min_inlier_ratio')}%). Inspect match-point distribution and consider stricter filtering or another image pair.")
        else:
            st.success(f"Inlier ratio meets the selected review threshold ({get_setting('min_inlier_ratio')}%). This is a screening rule, not a guarantee of absolute accuracy.")
        t1,t2,t3,t4=st.tabs(['Image Results','Correspondence Map','Detailed Metrics & Report','🛰️ Mission XML Metadata'])
        with t1:
            im1,im2,im3=st.columns(3)
            with im1:
                st.markdown('**Registered Image**'); st.image(result['warped'],use_container_width=True)
                st.download_button('Download Registered PNG',data=png_bytes(result['warped']),file_name='SETU_registered_source.png',mime='image/png',use_container_width=True)
            with im2:
                st.markdown('**Source + Reference Overlay**'); st.image(result['overlay'],use_container_width=True)
            with im3:
                st.markdown('**Source ↔ Reference Match Points**'); st.image(result['matches_vis'],use_container_width=True)
        with t2:
            st.markdown('#### Correspondence / spatial distribution map')
            st.image(result['matches_vis'],caption='Accepted RANSAC inlier correspondences. Inspect whether matches cover the image and avoid clusters.',use_container_width=True)
            st.markdown('#### Registered overlay map')
            st.image(result['overlay'],caption='50/50 registered-source and reference blend. Doubled edges indicate remaining misalignment.',use_container_width=True)
        with t3:
            m1,m2,m3,m4,m5=st.columns(5)
            m1.metric('Median residual',f"{result['median_error']:.3f} px" if np.isfinite(result['median_error']) else 'N/A')
            m2.metric('95th percentile error',f"{result['p95_error']:.3f} px" if np.isfinite(result['p95_error']) else 'N/A')
            m3.metric('4×4 grid coverage',f"{result['coverage']*100:.1f}%")
            m4.metric('Median X displacement',f"{result['shift_x_px']:.2f} px" if np.isfinite(result['shift_x_px']) else 'N/A')
            m5.metric('Median Y displacement',f"{result['shift_y_px']:.2f} px" if np.isfinite(result['shift_y_px']) else 'N/A')
            st.metric('Estimated transform scale (approx.)',f"{result['estimated_scale']:.4f}×" if np.isfinite(result['estimated_scale']) else 'N/A')
            st.markdown('**Estimated source → reference transformation matrix**')
            st.code(np.array2string(result['H'],precision=6,suppress_small=True),language='text')
            st.dataframe(result['points'].head(1000),use_container_width=True)
            st.download_button('Download Match Points (CSV)',data=result['points'].to_csv(index=False).encode(),file_name='SETU_match_points.csv',mime='text/csv')
            report={'timestamp_utc':result['timestamp_utc'],'transform_matrix':result['H'].tolist(),'fit_assessment':result['quality'],'match_status':result.get('match_status'),'confidence_score_percent':result.get('confidence_score',0),'matched_percentage':result.get('match_percentage',0),'operator_context':{'mode':result.get('registration_mode','Automatic'),'xml_driven_metadata':True,'automatic_engine':result.get('auto_attempt'),'configurations_tested':result.get('auto_candidates_tested'),'manual_parameters':result.get('manual_operator_context')},'source_xml_metadata':result.get('source_xml_metadata'),'reference_xml_metadata':result.get('reference_xml_metadata'),'limitations':['Inlier reprojection RMSE is not independent ground truth.','Authenticity checks do not establish whether content is genuine.']}
            metrics={k:result[k] for k in ['detector','model','keypoints_source','keypoints_reference','candidate_matches','inlier_count','inlier_ratio','rmse','median_error','p95_error','coverage','quality','confidence_score','match_percentage','match_status']}
            pdf=make_pdf(report,metrics,src_file_name,ref_file_name,png_bytes(result['warped']),result['points'].to_csv(index=False).encode())
            d1,d2=st.columns(2)
            with d1: st.download_button('Download Detailed Scientific Report (PDF)',data=pdf,file_name='SETU_registration_report.pdf',mime='application/pdf',use_container_width=True)
            with d2: st.download_button('Download Complete Run Summary (JSON)',data=json.dumps({'report':report,'metrics':metrics},indent=2,default=lambda x: None).encode(),file_name='SETU_run_summary.json',mime='application/json',use_container_width=True)
            xml_bundle={'source_xml':result.get('source_xml_metadata'),'reference_xml':result.get('reference_xml_metadata')}
            st.download_button('Download Parsed XML Metadata (JSON)',data=json.dumps(xml_bundle,indent=2,default=lambda x: None).encode(),file_name='SETU_xml_metadata.json',mime='application/json',use_container_width=True)
        with t4:
            st.markdown('### Mission metadata imported from XML')
            st.caption('Values shown here come from the uploaded mission sidecar XML. They provide acquisition/geometric context; image registration is still estimated from image correspondences.')
            xml_cols=st.columns(2)
            with xml_cols[0]:
                render_xml_interface(result.get('source_xml_metadata'), 'SOURCE XML')
            with xml_cols[1]:
                render_xml_interface(result.get('reference_xml_metadata'), 'REFERENCE XML')
            if not result.get('source_xml_metadata') and not result.get('reference_xml_metadata'):
                st.info('No XML sidecar was attached to this registration run.')

        if st.button('← BACK TO REGISTRATION SETTINGS'):
            st.session_state.page='Registration Lab'; st.rerun()

elif page=='Integrity Screening':
    st.markdown('### File integrity & provenance screening')
    st.warning('This is a conservative screening tool, not a fake-image/deepfake detector. A clean result does not prove authenticity, and missing metadata does not prove manipulation.')
    up=st.file_uploader('Upload an image or video to screen',type=['png','jpg','jpeg','tif','tiff','bmp','webp','mp4','mov','avi','mkv','webm'],key='integrity_upload')
    if up:
        try:
            im,info=image_from_upload(up); check=image_integrity_screen(up,im,info)
            c1,c2,c3=st.columns(3)
            c1.metric('Screening status',check['status']); c2.metric('Dimensions',f"{check['width']} × {check['height']}"); c3.metric('Metadata fields',check['exif_field_count'])
            st.image(im,caption='Uploaded media / extracted representative frame',use_container_width=True)
            st.markdown('#### Findings')
            for finding in check['findings']: st.write('• '+finding)
            if info.get('media_type','').startswith('Video'):
                st.write(f"Video frame count: {info.get('frame_count')} | FPS: {info.get('fps')} | Selected frame: {info.get('selected_frame')} | Duration: {info.get('duration_seconds')} s")
            st.markdown('#### File evidence')
            st.json({k:v for k,v in check.items() if k!='findings'})
            st.download_button('Download screening record (JSON)',data=json.dumps({'file_name':up.name,'screening':check,'media_info':{k:v for k,v in info.items() if k!='raw'}},indent=2).encode(),file_name='SETU_integrity_screening.json',mime='application/json')
            st.caption('For stronger provenance, compare official mission product IDs, signed manifests/checksums, original telemetry/metadata and trusted repository records. Pixel-only heuristics cannot reliably distinguish real from AI-generated or edited imagery.')
        except Exception as e: st.error(f'Screening failed: {e}')

else:
    st.markdown('<div class="hero"><div class="hero-kicker">ABOUT THE PLATFORM</div><div class="brand" style="font-size:40px">SOMSETU</div><p>Mission-aware lunar image correspondence, built to make complex scientific metadata understandable and registration practical.</p></div>',unsafe_allow_html=True)
    a1,a2=st.columns([1.1,0.9],gap='large')
    with a1:
        st.markdown('<div class="glass-card"><h3>How SOMSETU works</h3><p><b>1. Ingest:</b> source image + reference image and their mission XML sidecars.</p><p><b>2. Understand:</b> XML metadata is parsed for product identity, coordinates, resolution, spacecraft pose, solar geometry, acquisition information and processing history.</p><p><b>3. Normalize:</b> illumination normalization helps the feature engine handle different brightness conditions.</p><p><b>4. Correspond:</b> SIFT/AKAZE/ORB strategies are tested automatically.</p><p><b>5. Register:</b> RANSAC-based homography is attempted with a partial-affine fallback.</p><p><b>6. Evaluate:</b> inliers, residual error, coverage, displacement and the transformation matrix are reported.</p><p><b>7. Export:</b> registered image, correspondence CSV, PDF report, JSON summary and parsed XML metadata.</p></div>',unsafe_allow_html=True)
    with a2:
        st.markdown('<div class="auto-card"><h3>✨ Why it is different</h3><p><b>Mission metadata first:</b> the operator does not need to manually type Sun elevation, Sun azimuth, spacecraft altitude or corner coordinates when those values already exist in the XML.</p><p><b>Automatic when you want it, manual when you need it:</b> SOMSETU provides a simple automatic mode and a full Manual / Advanced mode with every important registration control exposed.</p><p><b>Traceable:</b> the original XML metadata and file hashes can travel with the result.</p><p><b>Scientific honesty:</b> a strong registration score is treated as a quality indicator, not as proof of absolute ground-truth accuracy.</p><p><b>Why try it:</b> it reduces operator burden while keeping the underlying evidence visible for review.</p></div>',unsafe_allow_html=True)
    st.markdown('### What SOMSETU is based on')
    b1,b2,b3,b4=st.columns(4)
    for col,icon,title,desc in [(b1,'🧾','Mission XML','Product, orbit, timing, geometry and coordinate metadata.'),(b2,'🔎','Local features','Image features and descriptor matching for correspondence.'),(b3,'📐','Robust geometry','RANSAC-based transformation estimation and residual analysis.'),(b4,'📊','Evidence & reports','Metrics, points, metadata, checksums and exportable reports.')]:
        with col: st.markdown(f'<div class="glass-card"><h4>{icon} {title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)
    st.warning('SOMSETU is a research prototype. No software can honestly promise 100% registration success on every image pair; real performance depends on overlap, texture, illumination, viewpoint and image quality. Mission validation and independent ground truth remain necessary.')
    st.markdown(f'<div class="panel"><b>Institution:</b> {PROJECT_UNIVERSITY}<br><b>Department:</b> {PROJECT_DEPARTMENT}<br><b>Team:</b> {TEAM_NAME}</div>',unsafe_allow_html=True)
st.markdown('<div style="text-align:center;margin-top:35px;padding:18px;border-top:1px solid rgba(130,180,255,.18);color:#9bb5da;font-size:12px;letter-spacing:1px">SOMSETU · SPACE-IMAGE ESTIMATION, TRACKING &amp; UNIFICATION &nbsp; | &nbsp; TEAM TEJASNET<br/>RESEARCH PROTOTYPE · VALIDATE BEFORE OPERATIONAL OR SCIENTIFIC CLAIMS</div>',unsafe_allow_html=True)
