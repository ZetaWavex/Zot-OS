import math

with open('kernel.cpp', 'r', encoding='gb2312') as f:
    content = f.read()

# Remove old draw_arc
helper_start = content.index('static void draw_arc(int cx, int cy')
bc = 0
p = helper_start
helper_end = -1
while p < len(content):
    if content[p] == '{': bc += 1
    elif content[p] == '}':
        bc -= 1
        if bc == 0:
            helper_end = p + 1
            break
    p += 1
content = content[:helper_start] + content[helper_end:]

# Generate 360 degree tables
sin_t = [int(round(140 * math.sin(math.radians(i)))) for i in range(360)]
cos_t = [int(round(140 * math.cos(math.radians(i)))) for i in range(360)]

def fmt_table(arr):
    return ', '.join(str(x) for x in arr)

arc_helper = f"""
static void draw_arc(int cx, int cy, int radius, int start_angle, int end_angle, int width, uint32_t color) {{
    static const short sin_t[360] = {{ {fmt_table(sin_t)} }};
    static const short cos_t[360] = {{ {fmt_table(cos_t)} }};
    int span = ((end_angle - start_angle) % 360 + 360) % 360;
    for (int a = 0; a <= span; a += 2) {{
        int angle = ((start_angle + a) % 360 + 360) % 360;
        int sx = cos_t[angle];
        int sy = sin_t[angle];
        for (int w = 0; w < width; ++w) {{
            int r = radius + w - width / 2;
            int x = cx + (sx * r / 140);
            int y = cy + (sy * r / 140);
            put_pixel(x, y, color);
        }}
    }}
}}
"""

insert_pos = content.index('static void draw_loading_screen() {')
content = content[:insert_pos] + arc_helper + content[insert_pos:]
print("draw_arc replaced with 360-degree table")

# Replace background color 0x0A1F44 -> 0x000000 in loading/shutdown
# But be careful not to replace other occurrences
# Just fix the specific ones in loading and shutdown

def replace_func(content, func_name, new_func):
    start = content.index(f'static void {func_name}() {{')
    bc = 0
    p = start
    end = -1
    while p < len(content):
        if content[p] == '{': bc += 1
        elif content[p] == '}':
            bc -= 1
            if bc == 0:
                end = p + 1
                break
        p += 1
    if end > 0:
        content = content[:start] + new_func + content[end:]
    return content

loading = r"""static void draw_loading_screen() {
    render_target = reinterpret_cast<uint32_t*>(backbuffer_address);
    fill_rect(0, 0, static_cast<int>(screen_width), static_cast<int>(screen_height), 0x000000);

    const int cx = static_cast<int>(screen_width / 2);
    const int cy = static_cast<int>(screen_height / 2);

    draw_logo(cx - 100, cy - 200, 200);

    const int acx = cx;
    const int acy = cy + 80;
    const int radius = 36;
    const int box = radius + 10;

    draw_text("Nova OS", cx - 32, acy + radius + 40, 1, 0xCCCCCC);
    present_backbuffer();

    for (int frame = 0; frame < 180; ++frame) {
        fill_rect(acx - box, acy - box, box * 2, box * 2, 0x000000);

        int base = frame * 8;
        draw_arc(acx, acy, radius, base, base + 90, 4, 0xFFFFFF);
        draw_arc(acx, acy, radius, base + 120, base + 210, 4, 0xFFFFFF);
        draw_arc(acx, acy, radius, base + 240, base + 330, 4, 0xFFFFFF);

        present_rect(acx - box, acy - box, box * 2, box * 2);
        wait_pit_ticks(3);
    }
}"""

shutdown = r"""static void draw_shutdown_screen() {
    render_target = reinterpret_cast<uint32_t*>(backbuffer_address);
    fill_rect(0, 0, static_cast<int>(screen_width), static_cast<int>(screen_height), 0x000000);

    const int cx = static_cast<int>(screen_width / 2);
    const int cy = static_cast<int>(screen_height / 2);

    draw_logo(cx - 100, cy - 200, 200);

    const int acx = cx;
    const int acy = cy + 80;
    const int radius = 36;
    const int box = radius + 10;

    draw_text("Shutting down...", cx - 48, acy + radius + 40, 1, 0xCCCCCC);
    present_backbuffer();

    for (int frame = 0; frame < 180; ++frame) {
        fill_rect(acx - box, acy - box, box * 2, box * 2, 0x000000);

        int base = frame * 8;
        draw_arc(acx, acy, radius, base, base + 90, 4, 0xFFFFFF);
        draw_arc(acx, acy, radius, base + 120, base + 210, 4, 0xFFFFFF);
        draw_arc(acx, acy, radius, base + 240, base + 330, 4, 0xFFFFFF);

        present_rect(acx - box, acy - box, box * 2, box * 2);
        wait_pit_ticks(3);
    }

    fill_rect(0, 0, static_cast<int>(screen_width), static_cast<int>(screen_height), 0x000000);
    draw_logo(cx - 100, cy - 100, 200);
    draw_text("Goodbye", cx - 32, cy + 40, 1, 0xCCCCCC);
    present_backbuffer();
    wait_pit_ticks(5);
}"""

content = replace_func(content, 'draw_loading_screen', loading)
content = replace_func(content, 'draw_shutdown_screen', shutdown)

with open('kernel.cpp', 'w', encoding='gb2312') as f:
    f.write(content)
print("Done - black background, 360-degree table")