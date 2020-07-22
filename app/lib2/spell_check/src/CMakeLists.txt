set(LIB_SOURCES
  spell.c
)

set(MAIN_SOURCES
  main.c
)

set(HEADERS 
  ${CONFIG_HEADER}
  spell.h
)

add_library(spell STATIC ${LIB_SOURCES} ${HEADERS})

add_executable(spell_check ${HEADERS} ${MAIN_SOURCES})
target_link_libraries(spell_check spell)

install(TARGETS spell
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/spell.h DESTINATION include)
