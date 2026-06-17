#import "@preview/zebra:0.1.0": qrcode

#set page(height: 5cm, width: 5cm, margin: 3mm)
#set text(font: "Helvetica Neue", size: 12pt)

#let hitster_card(
  back_link,
  middle_txt,
  top_txt,
  bot_txt,
  right_txt,
  left_txt,
) = {
  align(center + horizon)[
    #qrcode(back_link, height: 3cm)
  ]

  pagebreak()

  if top_txt != none {
    align(center + top)[
      #text(weight: 600)[
        #top_txt
      ]
    ]
  }

  if middle_txt != none {
    place(center + horizon)[
      #text(font: "Gotham", weight: 500, size: 32pt)[
        #middle_txt
      ]
    ]
  }

  if bot_txt != none {
    align(center + bottom)[
      #text(weight: 400)[
        #bot_txt
      ]
    ]
  }

  if right_txt != none {
    text(size: 9pt, weight: 300, fill: luma(66%))[
      #place(center + horizon, dx: 2.2cm)[
        #rotate(-90deg)[
          _ #right_txt _
        ]
      ]
    ]
  }

  if left_txt != none {
    text(size: 9pt, weight: 300, fill: luma(66%))[
      #place(center + horizon, dx: -2.2cm)[
        #rotate(-90deg)[
          _ #left_txt _
        ]
      ]
    ]
  }
}

#let hitster_deck(
  list_links,
  list_middle,
  list_top,
  list_bot,
  list_right,
  list_left,
) = {
  for i in range(list_links.len()) {
    hitster_card(
      list_links.at(i),
      list_middle.at(i),
      list_top.at(i),
      list_bot.at(i),
      list_right.at(i),
      list_left.at(i),
    )
  }
}

#let get_input_list(input_idx) = {
  return (
    sys.inputs.at("url_" + str(input_idx), default: "https://github.com/xmousset"),
    sys.inputs.at("year_" + str(input_idx), default: "2026"),
    sys.inputs.at("name_" + str(input_idx), default: "Amazing Track"),
    sys.inputs.at("artists_" + str(input_idx), default: "Great Artist"),
    sys.inputs.at("added_by_name_" + str(input_idx), default: "Added by: Friend"),
    sys.inputs.at("left_txt_" + str(input_idx), default: "Hitster Example"),
  )
}

// Main loop

#let nb_tracks = int(sys.inputs.at("nb_tracks", default: 1))

#for i in range(nb_tracks) {
  let (url, year, name, artists, added_by_name, left_txt) = get_input_list(i)
    hitster_card(
      url,
      year,
      name,
      artists,
      added_by_name,
      left_txt
    )
    if i < nb_tracks - 1 {
      pagebreak()
    }
  }
