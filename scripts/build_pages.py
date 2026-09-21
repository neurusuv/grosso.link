"""Generate the Grosso Link site pages (docs/*.md).

Run: python scripts/build_pages.py
"""
import html, io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
E = html.escape
CONTACT = 'info@grosso.link'
ADDRESS = ['Grosso Link GmbH', 'St. Jakobstrasse 58', '6330 Cham', 'Switzerland']


def write(name, body, title, desc, home=False):
    fm = f'---\ntitle: {json.dumps(title, ensure_ascii=False)}\ndescription: {json.dumps(desc, ensure_ascii=False)}\n'
    if home:
        fm += 'titleTemplate: Swiss Innovation\n'
    fm += 'aside: false\nsidebar: false\n---\n\n'
    path = os.path.join(DOCS, name + '.md')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(fm + body.strip() + '\n')


# 线描图标（24 网格，描边随 currentColor）
ICON = {
    'chip':   '<rect x="6" y="6" width="12" height="12" rx="1.5"/><rect x="9.5" y="9.5" width="5" height="5" rx=".5"/><path d="M9 2.5V6M15 2.5V6M9 18v3.5M15 18v3.5M2.5 9H6M2.5 15H6M18 9h3.5M18 15h3.5"/>',
    'wave':   '<path d="M2 12h3.5l2-6 3.5 12 3-9 2 3H22"/>',
    'clock':  '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    'thermo': '<path d="M10 13.5V4.5a2 2 0 1 1 4 0v9a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
    'prox':   '<path d="M3 12h6"/><circle cx="11" cy="12" r="1.5"/><path d="M15 8a5.5 5.5 0 0 1 0 8M18 5a10 10 0 0 1 0 14"/>',
    'leaf':   '<path d="M5 19C5 11 11 5 19 5c0 8-6 14-14 14z"/><path d="M5 19l8-8"/>',
    'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".8"/>',
    'fit':    '<path d="M4 4h7v7H4zM13 13h7v7h-7z"/><path d="M11 7.5h4.5V13"/>',
    'lock':   '<rect x="5" y="11" width="14" height="10" rx="1.5"/><path d="M8 11V7.5a4 4 0 0 1 8 0V11"/>',
    'layers': '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12.5l9 5 9-5"/><path d="M3 17l9 5 9-5"/>',
    'nav':    '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    'mixed':  '<path d="M2 15c2.5 0 2.5-6 5-6s2.5 6 5 6"/><path d="M12 15h2V9h2v6h2V9h2v6h2"/>',
}


def icon(name):
    return f'<svg class="gl-ico" viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg>'


def head(no, label, title, lead=None):
    lead_html = f'<p class="gl-head__lead">{E(lead)}</p>' if lead else ''
    return (f'<div class="gl-head"><div class="gl-head__meta"><span class="gl-head__no">{E(no)}</span>'
            f'<span class="gl-head__label">{E(label)}</span></div>'
            f'<div><h2 class="gl-h2">{title}</h2>{lead_html}</div></div>')


def feats(items, cols=3):
    return f'<div class="gl-feats gl-feats--{cols}">' + ''.join(
        f'<div class="gl-feat">{icon(ic)}<h3>{E(t)}</h3><p>{E(d)}</p></div>' for ic, t, d in items) + '</div>'


def bullets(items):
    return '<ul class="gl-list">' + ''.join(f'<li>{E(x)}</li>' for x in items) + '</ul>'


def page_hero(label, title, lead, art='phero'):
    return (f'<section class="gl-phero gl-bg gl-bg--{art}"><div class="gl-wrap">'
            f'<p class="gl-kicker"><span class="gl-swiss" aria-hidden="true"></span>{E(label)}</p>'
            f'<h1 class="gl-phero__title">{title}</h1><p class="gl-phero__lead">{E(lead)}</p></div></section>')


STEPS = '''<ol class="gl-steps">
<li><b>Specify</b><span>Your system, the quantity to sense, the interface and the power budget.</span></li>
<li><b>Architect</b><span>The right split between sensor, analog front-end, converter and on-chip logic.</span></li>
<li><b>Design &amp; verify</b><span>Full custom mixed-signal design, verified against a model of your system.</span></li>
<li><b>Qualify</b><span>Silicon validation, reliability qualification and production test.</span></li>
<li><b>Supply</b><span>Steady, long-term supply for the whole life of your platform.</span></li>
</ol>'''

def cta(art):
    return CTA.replace('gl-bg--contour', f'gl-bg--cta-{art}')


CTA = f'''
<section class="gl-cta gl-bg gl-bg--contour"><div class="gl-wrap gl-cta__in">
<div>
<p class="gl-kicker gl-kicker--inv"><span class="gl-swiss" aria-hidden="true"></span>Start a conversation</p>
<h2 class="gl-cta__title">Have a sensing problem that no standard part solves?</h2>
<p class="gl-cta__text">Tell us about your system. We will tell you whether a custom IC is the right answer.</p>
</div>
<a class="gl-btn gl-btn--inv" href="mailto:{CONTACT}">{CONTACT}<span class="gl-arrow" aria-hidden="true">→</span></a>
</div></section>
'''

# ---------------- 首页 ----------------
home = f'''
<section class="gl-hero gl-bg gl-bg--world-link"><div class="gl-wrap">
<p class="gl-kicker"><span class="gl-swiss" aria-hidden="true"></span>Grosso Link GmbH · Swiss Innovation since 2013</p>
<h1 class="gl-hero-title">Custom ASIC Partner for High&#8209;Performance Sensor &amp; Mixed&#8209;Signal ICs</h1>
<p class="gl-hero-lead">We design custom low-power sensor ICs that live inside our customers’ systems — for many years.</p>
<div class="gl-actions"><a class="gl-btn" href="/custom-asic">How we work<span class="gl-arrow" aria-hidden="true">→</span></a><a class="gl-btn gl-btn--ghost" href="/technology">Our technology</a></div>
</div></section>
<div class="gl-band"><span>Precision</span><i></i><span>Integration</span><i></i><span>Reliability</span></div>

<section class="gl-section"><div class="gl-wrap">
{head('01', 'What we do', 'One chip, designed for one system', 'Sensor, analog front-end, converter and digital control — integrated on a single piece of silicon that is built around your product, and nobody else’s.')}
{feats([('chip', 'Custom sensor ICs', 'Sensor, analog front-end, ADC and digital control on one chip, built around your system and your interface.'),
        ('wave', 'Precision mixed-signal', 'A high-precision analog signal chain with a low 1/f-noise front-end — the foundation of accurate, low-power sensing.'),
        ('clock', 'Long-life reliability', 'Wide-temperature operation and long-term reliability designed in from the start, for platforms that ship for many years.')])}
</div></section>

<section class="gl-art gl-bg gl-bg--chip"><div class="gl-wrap gl-art__in">
<p class="gl-kicker">Inside the silicon</p>
<h2 class="gl-h2">Every block on the die earns its place</h2>
</div></section>

<section class="gl-section"><div class="gl-wrap">
{head('02', 'Where our silicon works', 'Sensing for industrial and commercial systems')}
{feats([('thermo', 'Precision temperature monitoring', 'High-accuracy digital temperature sensing with µA-class standby current — in volume production today.'),
        ('prox', 'Proximity and position sensing', 'Robust position and proximity sensing front-ends for process equipment and industrial automation.'),
        ('leaf', 'Environmental and agricultural monitoring', 'Low-power sensor nodes that run for years in the field, from greenhouses to open land.')])}
</div></section>

<section class="gl-statement gl-bg gl-bg--quote"><div class="gl-wrap">
<p class="gl-quote">“L’esprit de collaboration et l’envie d’explorer de nouvelles opportunités ont été soulignés comme étant les forces motrices des entreprises innovantes.”</p>
<span class="gl-quote-by">Swiss Innovation</span>
</div></section>

''' + cta('cham-panorama')
write('index', home, 'Grosso Link', 'Grosso Link — Swiss Innovation. Custom ASIC partner for high-performance sensor and mixed-signal ICs: precision, integration, reliability.', home=True)

# ---------------- Technology ----------------
tech = page_hero('Technology', 'Two pillars, one decade of sensor silicon',
                 'Navigation-grade sensing IP and high-performance mixed-signal design — built up over more than ten years of sensor IC development.', 'wafer-probe') + f'''

<section class="gl-section"><div class="gl-wrap">
{head('01', 'Core technology', 'Built on two pillars')}
<div class="gl-pillars2">
<div class="gl-pcard"><div class="gl-pcard__top">{icon('nav')}<span class="gl-pcard__tag">Pillar 1</span></div>
<h3>Navigation &amp; Position Sensing</h3>
{bullets(['Proven navigation sensing IP from previous-generation products', 'Robust sensing algorithms embedded on-chip', 'The foundation for custom proximity and position sensing ASICs'])}
</div>
<div class="gl-pcard"><div class="gl-pcard__top">{icon('mixed')}<span class="gl-pcard__tag">Pillar 2</span></div>
<h3>High-Performance Mixed-Signal</h3>
{bullets(['High-precision analog signal chain with a low 1/f-noise front-end', 'Sensor, ADC and digital control integrated on one chip', 'Wide-temperature, long-life reliability by design'])}
</div>
</div>
</div></section>

<section class="gl-section gl-section--ice"><div class="gl-wrap">
{head('02', 'Proof point', 'A temperature sensor in volume production', 'Both pillars in one chip: accurate across the full temperature range, frugal enough for battery-powered systems, and simple to calibrate in production.')}
<div class="gl-stats">
<div class="gl-stat"><b>Full range</b><span>accuracy across the whole operating temperature range — not only at room temperature</span></div>
<div class="gl-stat"><b>µA-class</b><span>standby current, for systems that run for years on one battery</span></div>
<div class="gl-stat"><b>1-point</b><span>calibration in production instead of multi-point trimming</span></div>
</div>
</div></section>

<section class="gl-section"><div class="gl-wrap">
{head('03', 'Next', 'Industrial proximity sensing', 'A custom inductive proximity front-end for process equipment and industrial robotics, in development together with an industrial customer.')}
{feats([('target', 'Programmable thresholds', 'Switching thresholds and hysteresis set by the system, not fixed in the part.'),
        ('thermo', 'Temperature compensation', 'Compensated on-chip, so the switching point stays put from cold start to full load.'),
        ('clock', 'Built for 24/7', 'Designed for continuous operation in harsh industrial environments.')])}
</div></section>
''' + cta('wafer-probe')
write('technology', tech, 'Technology', 'Navigation and position sensing IP, and high-performance mixed-signal design: low 1/f-noise front-ends, sensor + ADC + digital control on one chip, long-life reliability.')

# ---------------- Custom ASIC（合作方式） ----------------
asic = page_hero('Custom ASIC', 'We do not build catalog parts',
                 'Every chip we design is made for one customer, one system — and kept confidential for the life of the platform.', 'custom-asic-farm') + f'''

<section class="gl-section"><div class="gl-wrap">
{head('01', 'Our model', 'What a Grosso Link chip means for you')}
{feats([('fit', 'Custom design', 'Built around your own protocol and system architecture — the chip speaks your system’s language, not a generic standard.'),
        ('target', 'Deep system fit', 'Exactly the features your system needs, nothing else: higher accuracy, a direct line to your engineering team, faster delivery.'),
        ('lock', 'Confidential by default', 'Every engagement is exclusive and strictly confidential. We never show one customer’s design to another.'),
        ('layers', 'For the life of the platform', 'Once designed in, the chip ships steadily for the whole life of your product, with long-term supply planned from day one.')], 4)}
</div></section>

<section class="gl-section gl-section--ice"><div class="gl-wrap gl-split">
<div>
<p class="gl-kicker">Why a custom IC</p>
<h2 class="gl-h2">A part nobody else can buy</h2>
<p class="gl-body">Standard parts are designed for everyone, so they fit no one exactly. A custom sensor IC removes the external components, the conversions and the compromises between your sensor and your system — and turns them into a single, qualified chip.</p>
</div>
<div>
<p class="gl-kicker">What we need from you</p>
{bullets(['The physical quantity you need to sense, and how precisely', 'Your system interface and power budget', 'Expected lifetime, environment and yearly volume'])}
</div>
</div></section>

<section class="gl-section"><div class="gl-wrap">
{head('02', 'The process', 'From your system to your silicon')}
{STEPS}
</div></section>
''' + cta('custom-asic-farm')
write('custom-asic', asic, 'Custom ASIC', 'We do not build catalog parts: every Grosso Link chip is a custom sensor ASIC designed for one customer, under strict confidentiality, for the life of the platform.')

# ---------------- About us ----------------
about = page_hero('About us', 'A Swiss IC design company',
                  'Headquartered in Cham, founded in the canton of Neuchâtel in 2013.', 'neuchatel') + f'''

<section class="gl-section"><div class="gl-wrap gl-split gl-split--wide">
<div>
<p class="gl-kicker">Our story</p>
<h2 class="gl-h2">From navigation research to custom silicon</h2>
</div>
<div class="gl-prose">

Grosso Link GmbH develops low-power sensor and mixed-signal ICs for industrial and commercial customers, designed around each customer’s own system.

Our work grew out of navigation and position-sensing research, including a history of navigation-algorithm collaboration with EPFL, and of precision temperature sensing. The same foundations — a low-noise analog front-end, on-chip algorithms and long-life reliability — now go into every custom ASIC we build.

Our mission is simple: design custom sensor ICs that live inside our customers’ systems — for many years.

</div>
</div></section>

<section class="gl-art gl-bg gl-bg--epfl"><div class="gl-wrap gl-art__in">
<p class="gl-kicker">Swiss roots</p>
<h2 class="gl-h2">Lausanne, Neuchâtel, Cham</h2>
<p class="gl-body">Algorithm collaboration with EPFL on Lake Geneva, a founding in the watchmaking canton of Neuchâtel, and a headquarters in Cham — three Swiss places, one standard of precision.</p>
</div></section>

<section class="gl-section gl-section--ice"><div class="gl-wrap">
<div class="gl-facts">
<div><b>Headquarters</b><span>St. Jakobstrasse 58<br>6330 Cham, Switzerland</span></div>
<div><b>Founded</b><span>2013<br>Neuchâtel</span></div>
<div><b>Focus</b><span>Low-power sensor &amp;<br>mixed-signal ICs</span></div>
<div><b>Model</b><span>Custom ASIC,<br>one customer per chip</span></div>
</div>
</div></section>
''' + cta('neuchatel')
write('about-us', about, 'About us', 'Grosso Link is a Swiss IC design company headquartered in Cham, founded in 2013, developing low-power sensor and mixed-signal custom ASICs.')

# ---------------- Contact ----------------
contact = page_hero('Contact', 'Let’s talk about your system',
                    'For custom IC projects, partnerships and general enquiries.', 'cham-panorama') + f'''

<section class="gl-section"><div class="gl-wrap gl-contact">
<div class="gl-contact__main">
<p class="gl-kicker">Write to us</p>
<a class="gl-contact__mail" href="mailto:{CONTACT}">{CONTACT}<span class="gl-arrow" aria-hidden="true">→</span></a>
<p class="gl-body">Tell us about your system in a few lines. Every enquiry is treated confidentially.</p>
<div class="gl-facts gl-facts--2 gl-contact__facts">
<div><b>Address</b><span>{'<br>'.join(E(x) for x in ADDRESS)}</span></div>
<div><b>Where</b><span>Cham, canton of Zug<br>on the shore of Lake Zug</span></div>
</div>
</div>
<aside class="gl-contact__side">
<p class="gl-kicker">What helps us answer</p>
<ol class="gl-contact__list">
<li><b>Your application</b><span>What the system does, and where the chip will live.</span></li>
<li><b>What you need to sense</b><span>The physical quantity, the range and the accuracy you need.</span></li>
<li><b>Interface &amp; power</b><span>How the chip talks to your system, and its power budget.</span></li>
<li><b>Volume &amp; lifetime</b><span>Expected yearly volume and how long the platform will ship.</span></li>
</ol>
</aside>
</div></section>
'''
write('contact', contact, 'Contact', 'Contact Grosso Link, St. Jakobstrasse 58, 6330 Cham, Switzerland, for custom sensor and mixed-signal IC projects.')

# ---------------- 404 ----------------
nf = page_hero('404', 'Page not found', 'This page has moved.') + '''
<section class="gl-section"><div class="gl-wrap"><a class="gl-btn" href="/">Back to the home page</a></div></section>
'''
write('404', nf, 'Page not found', 'Page not found')
print('pages written')
