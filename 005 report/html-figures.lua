-- Bytter ut rå HTML <img>-tagger med native pandoc Image-elementer,
-- slik at figurene kommer med ved konvertering til docx.

local function url_decode(s)
  return (s:gsub("%%(%x%x)", function(hex)
    return string.char(tonumber(hex, 16))
  end))
end

local function img_from_html(html)
  local src = html:match('<img[^>]-src="([^"]+)"')
  if not src then return nil end

  local alt   = html:match('<img[^>]-alt="([^"]*)"') or ""
  local width = html:match('<img[^>]-width="([^"]+)"')

  src = url_decode(src)

  local attrs = {}
  if width then attrs.width = width end

  return pandoc.Image(
    { pandoc.Str(alt) },
    src,
    "",
    pandoc.Attr("", {}, attrs)
  )
end

function RawInline(el)
  if el.format ~= "html" then return nil end
  return img_from_html(el.text)
end

function RawBlock(el)
  if el.format ~= "html" then return nil end
  local img = img_from_html(el.text)
  if not img then return nil end
  return pandoc.Para({ img })
end
