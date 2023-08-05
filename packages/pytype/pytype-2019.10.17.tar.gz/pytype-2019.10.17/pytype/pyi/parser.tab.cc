// A Bison parser, made by GNU Bison 3.3.2.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015, 2018-2019 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// Undocumented macros, especially those whose name start with YY_,
// are private implementation details.  Do not rely on them.


// Take the name prefix into account.
#define yylex   pytypelex



#include "parser.tab.hh"


// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:435

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 73 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:435


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

// Whether we are compiled with exception support.
#ifndef YY_EXCEPTIONS
# if defined __GNUC__ && !defined __EXCEPTIONS
#  define YY_EXCEPTIONS 0
# else
#  define YY_EXCEPTIONS 1
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (false)
# endif


// Suppress unused-variable warnings by "using" E.
#define YYUSE(E) ((void) (E))

// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << '\n';                       \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yystack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE (Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void> (0)
# define YY_STACK_PRINT()                static_cast<void> (0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:510
namespace pytype {
#line 168 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:510

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr;
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              else
                goto append;

            append:
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }


  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
    :
#if PYTYPEDEBUG
      yydebug_ (false),
      yycdebug_ (&std::cerr),
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}

  parser::syntax_error::~syntax_error () YY_NOEXCEPT YY_NOTHROW
  {}

  /*---------------.
  | Symbol types.  |
  `---------------*/

  // basic_symbol.
#if 201103L <= YY_CPLUSPLUS
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (basic_symbol&& that)
    : Base (std::move (that))
    , value (std::move (that.value))
    , location (std::move (that.location))
  {}
#endif

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& that)
    : Base (that)
    , value (that.value)
    , location (that.location)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_MOVE_REF (location_type) l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_RVREF (semantic_type) v, YY_RVREF (location_type) l)
    : Base (t)
    , value (YY_MOVE (v))
    , location (YY_MOVE (l))
  {}

  template <typename Base>
  bool
  parser::basic_symbol<Base>::empty () const YY_NOEXCEPT
  {
    return Base::type_get () == empty_symbol;
  }

  template <typename Base>
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move (s);
    value = YY_MOVE (s.value);
    location = YY_MOVE (s.location);
  }

  // by_type.
  parser::by_type::by_type ()
    : type (empty_symbol)
  {}

#if 201103L <= YY_CPLUSPLUS
  parser::by_type::by_type (by_type&& that)
    : type (that.type)
  {
    that.clear ();
  }
#endif

  parser::by_type::by_type (const by_type& that)
    : type (that.type)
  {}

  parser::by_type::by_type (token_type t)
    : type (yytranslate_ (t))
  {}

  void
  parser::by_type::clear ()
  {
    type = empty_symbol;
  }

  void
  parser::by_type::move (by_type& that)
  {
    type = that.type;
    that.clear ();
  }

  int
  parser::by_type::type_get () const YY_NOEXCEPT
  {
    return type;
  }


  // by_state.
  parser::by_state::by_state () YY_NOEXCEPT
    : state (empty_state)
  {}

  parser::by_state::by_state (const by_state& that) YY_NOEXCEPT
    : state (that.state)
  {}

  void
  parser::by_state::clear () YY_NOEXCEPT
  {
    state = empty_state;
  }

  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  parser::by_state::by_state (state_type s) YY_NOEXCEPT
    : state (s)
  {}

  parser::symbol_number_type
  parser::by_state::type_get () const YY_NOEXCEPT
  {
    if (state == empty_state)
      return empty_symbol;
    else
      return yystos_[state];
  }

  parser::stack_symbol_type::stack_symbol_type ()
  {}

  parser::stack_symbol_type::stack_symbol_type (YY_RVREF (stack_symbol_type) that)
    : super_type (YY_MOVE (that.state), YY_MOVE (that.value), YY_MOVE (that.location))
  {
#if 201103L <= YY_CPLUSPLUS
    // that is emptied.
    that.state = empty_state;
#endif
  }

  parser::stack_symbol_type::stack_symbol_type (state_type s, YY_MOVE_REF (symbol_type) that)
    : super_type (s, YY_MOVE (that.value), YY_MOVE (that.location))
  {
    // that is emptied.
    that.type = empty_symbol;
  }

#if YY_CPLUSPLUS < 201103L
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    // that is emptied.
    that.state = empty_state;
    return *this;
  }
#endif

  template <typename Base>
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.type_get ())
    {
      case 3: // NAME
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 402 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 4: // NUMBER
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 408 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 5: // STRING
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 414 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 6: // LEXERROR
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 420 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 48: // start
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 426 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 49: // unit
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 432 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 50: // alldefs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 438 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 52: // classdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 444 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 53: // class_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 450 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 54: // parents
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 456 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 55: // parent_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 462 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 56: // parent
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 468 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 57: // maybe_class_funcs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 474 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 58: // class_funcs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 480 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 59: // funcdefs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 486 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 60: // if_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 492 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 61: // if_and_elifs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 62: // class_if_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 504 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 63: // class_if_and_elifs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 510 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 64: // if_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 516 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 65: // elif_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 522 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 66: // else_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 528 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 67: // condition
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 534 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 68: // version_tuple
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 540 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 69: // condition_op
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.str)); }
#line 546 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 70: // constantdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 552 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 71: // importdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 558 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 72: // import_items
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 564 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 73: // import_item
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 570 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 74: // import_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 576 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 75: // from_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 582 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 76: // from_items
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 588 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 77: // from_item
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 594 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 78: // alias_or_constant
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 600 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 79: // maybe_string_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 606 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 80: // string_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 612 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 81: // typevardef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 618 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 82: // typevar_args
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 83: // typevar_kwargs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 630 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 84: // typevar_kwarg
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 636 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 85: // funcdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 642 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 86: // funcname
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 648 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 87: // decorators
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 654 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 88: // decorator
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 660 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 89: // maybe_async
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 90: // params
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 672 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 91: // param_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 678 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 92: // param
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 684 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 93: // param_type
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 690 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 94: // param_default
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 696 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 95: // param_star_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 702 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 96: // return
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 708 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 98: // maybe_body
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 714 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 100: // body
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 720 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 101: // body_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 726 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 102: // type_parameters
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 732 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 103: // type_parameter
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 738 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 104: // maybe_type_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 744 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 105: // type_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 750 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 106: // type
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 756 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 107: // named_tuple_fields
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 762 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 108: // named_tuple_field_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 768 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 109: // named_tuple_field
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 774 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 111: // coll_named_tuple_fields
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 780 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 112: // coll_named_tuple_field_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 786 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 113: // coll_named_tuple_field
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 792 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 114: // type_tuple_elements
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 798 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 115: // type_tuple_literal
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 804 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 116: // dotted_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 810 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 117: // getitem_key
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 816 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      case 118: // maybe_number
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:652
        { Py_CLEAR((yysym.value.obj)); }
#line 822 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:652
        break;

      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo,
                                     const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    symbol_number_type yytype = yysym.type_get ();
#if defined __GNUC__ && ! defined __clang__ && ! defined __ICC && __GNUC__ * 100 + __GNUC_MINOR__ <= 408
    // Avoid a (spurious) G++ 4.8 warning about "array subscript is
    // below array bounds".
    if (yysym.empty ())
      std::abort ();
#endif
    yyo << (yytype < yyntokens_ ? "token" : "nterm")
        << ' ' << yytname_[yytype] << " ("
        << yysym.location << ": ";
    YYUSE (yytype);
    yyo << ')';
  }
#endif

  void
  parser::yypush_ (const char* m, YY_MOVE_REF (stack_symbol_type) sym)
  {
    if (m)
      YY_SYMBOL_PRINT (m, sym);
    yystack_.push (YY_MOVE (sym));
  }

  void
  parser::yypush_ (const char* m, state_type s, YY_MOVE_REF (symbol_type) sym)
  {
#if 201103L <= YY_CPLUSPLUS
    yypush_ (m, stack_symbol_type (s, std::move (sym)));
#else
    stack_symbol_type ss (s, sym);
    yypush_ (m, ss);
#endif
  }

  void
  parser::yypop_ (int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - yyntokens_] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - yyntokens_];
  }

  bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::operator() ()
  {
    return parse ();
  }

  int
  parser::parse ()
  {
    // State.
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

#if YY_EXCEPTIONS
    try
#endif // YY_EXCEPTIONS
      {
    YYCDEBUG << "Starting parse\n";


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, YY_MOVE (yyla));

  /*-----------------------------------------------.
  | yynewstate -- push a new symbol on the stack.  |
  `-----------------------------------------------*/
  yynewstate:
    YYCDEBUG << "Entering state " << yystack_[0].state << '\n';

    // Accept?
    if (yystack_[0].state == yyfinal_)
      YYACCEPT;

    goto yybackup;


  /*-----------.
  | yybackup.  |
  `-----------*/
  yybackup:
    // Try to take a decision without lookahead.
    yyn = yypact_[yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token: ";
#if YY_EXCEPTIONS
        try
#endif // YY_EXCEPTIONS
          {
            yyla.type = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
#if YY_EXCEPTIONS
        catch (const syntax_error& yyexc)
          {
            YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
            error (yyexc);
            goto yyerrlab1;
          }
#endif // YY_EXCEPTIONS
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.type_get ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.type_get ())
      goto yydefault;

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", yyn, YY_MOVE (yyla));
    goto yynewstate;


  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;


  /*-----------------------------.
  | yyreduce -- do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_ (yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Default location.
      {
        stack_type::slice range (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, range, yylen);
        yyerror_range[1].location = yylhs.location;
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
#if YY_EXCEPTIONS
      try
#endif // YY_EXCEPTIONS
        {
          switch (yyn)
            {
  case 2:
#line 134 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1083 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 3:
#line 135 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 4:
#line 139 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1095 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 5:
#line 143 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1101 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 6:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1107 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 7:
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1113 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 8:
#line 146 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1124 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 9:
#line 152 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1130 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 10:
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1136 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 11:
#line 154 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1146 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 12:
#line 159 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1152 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 15:
#line 171 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNN)", (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1161 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 16:
#line 178 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1174 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 17:
#line 189 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1180 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 18:
#line 190 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1186 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 19:
#line 191 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1192 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 20:
#line 195 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1198 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 21:
#line 196 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1204 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 22:
#line 200 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1210 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 23:
#line 201 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1216 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 24:
#line 202 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyString_FromString("NamedTuple"); }
#line 1222 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 25:
#line 206 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1228 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 26:
#line 207 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1234 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 27:
#line 208 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1240 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 28:
#line 212 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1246 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 29:
#line 213 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1252 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 30:
#line 217 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1258 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 31:
#line 218 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1268 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 32:
#line 223 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1274 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 33:
#line 224 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1284 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 34:
#line 229 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1290 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 35:
#line 230 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1296 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 36:
#line 235 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1304 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 37:
#line 238 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1310 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 38:
#line 243 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1318 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 39:
#line 247 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1326 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 40:
#line 266 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1334 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 41:
#line 269 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1340 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 42:
#line 274 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1348 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 43:
#line 278 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1356 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 44:
#line 290 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1362 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 45:
#line 294 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1368 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 46:
#line 298 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 47:
#line 302 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1382 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 48:
#line 305 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1390 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 49:
#line 308 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 50:
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1406 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 51:
#line 314 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1412 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 52:
#line 315 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1418 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 53:
#line 316 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1424 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 54:
#line 321 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1430 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 55:
#line 322 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1436 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 56:
#line 323 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1444 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 57:
#line 329 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.str) = "<"; }
#line 1450 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 58:
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.str) = ">"; }
#line 1456 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 59:
#line 331 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.str) = "<="; }
#line 1462 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 60:
#line 332 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.str) = ">="; }
#line 1468 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 61:
#line 333 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.str) = "=="; }
#line 1474 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 62:
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.str) = "!="; }
#line 1480 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 63:
#line 338 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1489 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 64:
#line 342 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 65:
#line 346 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1507 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 66:
#line 350 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1516 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 67:
#line 354 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1525 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 68:
#line 358 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1534 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 69:
#line 362 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1543 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 70:
#line 369 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1552 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 71:
#line 373 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1561 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 72:
#line 377 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1572 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 73:
#line 383 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1583 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 74:
#line 392 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 75:
#line 393 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1595 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 76:
#line 397 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1601 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 77:
#line 398 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 78:
#line 403 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1613 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 79:
#line 404 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1622 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 80:
#line 411 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1628 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 81:
#line 412 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1634 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 82:
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1640 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 83:
#line 417 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1646 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 84:
#line 418 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 85:
#line 422 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1658 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 86:
#line 423 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 87:
#line 426 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 88:
#line 429 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1682 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 89:
#line 432 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1690 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 90:
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1696 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 91:
#line 439 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1702 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 92:
#line 440 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)); }
#line 1708 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 93:
#line 444 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1714 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 94:
#line 445 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1720 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 95:
#line 449 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1726 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 96:
#line 450 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1732 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 97:
#line 454 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1741 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 98:
#line 461 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1747 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 99:
#line 462 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1753 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 100:
#line 463 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1759 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 101:
#line 464 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1765 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 102:
#line 468 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1771 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 103:
#line 469 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1777 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 104:
#line 473 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1783 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 105:
#line 475 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1789 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 106:
#line 479 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[8].value.obj), (yystack_[7].value.obj), (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      //
      // TODO(dbaum): Consider making this smarter and only ignoring decorators
      // when they are empty.  Making decorators non-nullable and having two
      // productions for funcdef would be a reasonable solution.
      yylhs.location.begin = yystack_[6].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1808 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 107:
#line 496 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1814 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 108:
#line 497 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 109:
#line 501 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1826 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 110:
#line 502 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1832 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 111:
#line 506 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1838 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 112:
#line 510 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_True; }
#line 1844 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 113:
#line 511 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_False; }
#line 1850 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 114:
#line 515 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1856 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 115:
#line 516 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1862 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 116:
#line 528 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1868 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 117:
#line 529 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1874 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 118:
#line 533 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1880 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 119:
#line 534 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1886 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 120:
#line 535 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1892 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 121:
#line 536 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1898 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 122:
#line 540 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1904 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 123:
#line 541 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1910 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 124:
#line 545 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1916 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 125:
#line 546 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1922 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 126:
#line 547 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1928 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 127:
#line 548 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1934 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 128:
#line 552 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1940 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 129:
#line 553 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1946 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 130:
#line 557 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1952 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 131:
#line 558 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1958 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 132:
#line 562 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { Py_DecRef((yystack_[0].value.obj)); }
#line 1964 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 133:
#line 566 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1970 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 134:
#line 567 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1976 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 135:
#line 568 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 1982 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 143:
#line 582 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1988 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 144:
#line 583 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1994 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 145:
#line 587 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2000 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 146:
#line 588 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2006 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 147:
#line 589 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2012 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 148:
#line 593 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2018 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 149:
#line 594 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2024 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 150:
#line 598 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2030 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 151:
#line 599 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2036 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 152:
#line 601 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2042 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 153:
#line 602 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2048 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 154:
#line 604 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2057 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 155:
#line 611 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2063 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 156:
#line 612 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 2069 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 157:
#line 616 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2075 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 158:
#line 617 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2081 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 159:
#line 621 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2090 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 160:
#line 625 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), PyList_New(0));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2099 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 161:
#line 629 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2108 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 162:
#line 633 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2117 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 163:
#line 637 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2126 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 164:
#line 641 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2132 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 165:
#line 642 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2138 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 166:
#line 643 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2144 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 167:
#line 644 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2150 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 168:
#line 645 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2156 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 169:
#line 649 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2162 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 170:
#line 650 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 2168 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 171:
#line 654 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2174 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 172:
#line 655 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2180 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 173:
#line 659 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2186 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 176:
#line 668 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2192 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 177:
#line 669 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = PyList_New(0); }
#line 2198 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 178:
#line 673 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2206 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 179:
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2212 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 180:
#line 680 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2218 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 181:
#line 687 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 182:
#line 688 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 183:
#line 697 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2239 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 184:
#line 702 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2248 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 185:
#line 708 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2257 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 186:
#line 715 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2263 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 187:
#line 716 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2279 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 188:
#line 730 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2285 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 189:
#line 731 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2295 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 190:
#line 736 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2305 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 191:
#line 744 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2311 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;

  case 192:
#line 745 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:919
    { (yylhs.value.obj) = NULL; }
#line 2317 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
    break;


#line 2321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:919
            default:
              break;
            }
        }
#if YY_EXCEPTIONS
      catch (const syntax_error& yyexc)
        {
          YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
          error (yyexc);
          YYERROR;
        }
#endif // YY_EXCEPTIONS
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;
      YY_STACK_PRINT ();

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, YY_MOVE (yylhs));
    }
    goto yynewstate;


  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        error (yyla.location, yysyntax_error_ (yystack_[0].state, yyla));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.type_get () == yyeof_)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:
    /* Pacify compilers when the user code never invokes YYERROR and
       the label yyerrorlab therefore never appears in user code.  */
    if (false)
      YYERROR;

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    goto yyerrlab1;


  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    {
      stack_symbol_type error_token;
      for (;;)
        {
          yyn = yypact_[yystack_[0].state];
          if (!yy_pact_value_is_default_ (yyn))
            {
              yyn += yyterror_;
              if (0 <= yyn && yyn <= yylast_ && yycheck_[yyn] == yyterror_)
                {
                  yyn = yytable_[yyn];
                  if (0 < yyn)
                    break;
                }
            }

          // Pop the current state because it cannot handle the error token.
          if (yystack_.size () == 1)
            YYABORT;

          yyerror_range[1].location = yystack_[0].location;
          yy_destroy_ ("Error: popping", yystack_[0]);
          yypop_ ();
          YY_STACK_PRINT ();
        }

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = yyn;
      yypush_ ("Shifting", YY_MOVE (error_token));
    }
    goto yynewstate;


  /*-------------------------------------.
  | yyacceptlab -- YYACCEPT comes here.  |
  `-------------------------------------*/
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;


  /*-----------------------------------.
  | yyabortlab -- YYABORT comes here.  |
  `-----------------------------------*/
  yyabortlab:
    yyresult = 1;
    goto yyreturn;


  /*-----------------------------------------------------.
  | yyreturn -- parsing is finished, return the result.  |
  `-----------------------------------------------------*/
  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
#if YY_EXCEPTIONS
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack\n";
        // Do not try to display the values of the reclaimed symbols,
        // as their printers might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
#endif // YY_EXCEPTIONS
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what ());
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (state_type yystate, const symbol_type& yyla) const
  {
    // Number of reported tokens (one for the "unexpected", one per
    // "expected").
    size_t yycount = 0;
    // Its maximum.
    enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
    // Arguments of yyformat.
    char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];

    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state
         merging (from LALR or IELR) and default reductions corrupt the
         expected token list.  However, the list is correct for
         canonical LR with one exception: it will still contain any
         token that will not be accepted due to an error action in a
         later state.
    */
    if (!yyla.empty ())
      {
        int yytoken = yyla.type_get ();
        yyarg[yycount++] = yytname_[yytoken];
        int yyn = yypact_[yystate];
        if (!yy_pact_value_is_default_ (yyn))
          {
            /* Start YYX at -YYN if negative to avoid negative indexes in
               YYCHECK.  In other words, skip the first -YYN actions for
               this state because they are default actions.  */
            int yyxbegin = yyn < 0 ? -yyn : 0;
            // Stay within bounds of both yycheck and yytname.
            int yychecklim = yylast_ - yyn + 1;
            int yyxend = yychecklim < yyntokens_ ? yychecklim : yyntokens_;
            for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
              if (yycheck_[yyx + yyn] == yyx && yyx != yyterror_
                  && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
                {
                  if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                    {
                      yycount = 1;
                      break;
                    }
                  else
                    yyarg[yycount++] = yytname_[yyx];
                }
          }
      }

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
      default: // Avoid compiler warnings.
        YYCASE_ (0, YY_("syntax error"));
        YYCASE_ (1, YY_("syntax error, unexpected %s"));
        YYCASE_ (2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_ (3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_ (4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_ (5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    size_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += yytnamerr_ (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short parser::yypact_ninf_ = -253;

  const short parser::yytable_ninf_ = -192;

  const short
  parser::yypact_[] =
  {
       5,  -253,   107,   134,   375,   141,  -253,  -253,   -14,   140,
      40,   166,    12,  -253,  -253,   369,   148,  -253,  -253,  -253,
    -253,  -253,     9,  -253,   242,   132,  -253,   157,  -253,    40,
     335,   343,   254,  -253,    80,    69,   179,   184,  -253,    40,
     200,   205,   195,  -253,   166,  -253,   246,  -253,   217,   225,
     242,  -253,   266,   338,  -253,  -253,   231,   245,   242,   287,
     114,  -253,    45,   269,   177,    40,    40,  -253,  -253,  -253,
    -253,   296,  -253,  -253,   303,    14,   308,   166,  -253,  -253,
     310,     7,    76,  -253,     7,   335,   299,   309,  -253,   -10,
     144,   336,   345,   288,   242,   242,   330,  -253,   176,   358,
     242,   324,   353,  -253,   317,   365,  -253,   372,   217,  -253,
     352,  -253,   385,   378,  -253,   360,  -253,   342,   373,   371,
    -253,  -253,   408,  -253,  -253,  -253,  -253,   396,  -253,  -253,
    -253,   139,  -253,   378,   379,  -253,     7,    41,   378,  -253,
    -253,   278,  -253,  -253,  -253,   380,   381,   382,  -253,   403,
    -253,   378,  -253,  -253,  -253,   153,   242,   383,  -253,   385,
     384,     8,   211,   242,   386,  -253,   418,  -253,   242,  -253,
     250,   115,   367,   420,   388,   423,   364,  -253,   139,   378,
    -253,   302,   304,  -253,    33,   389,   390,  -253,   387,   391,
     393,   385,   182,   392,   262,   397,  -253,  -253,   385,   385,
    -253,  -253,   385,  -253,  -253,  -253,   341,  -253,   378,    90,
    -253,   400,    46,  -253,  -253,    24,  -253,  -253,  -253,  -253,
     401,  -253,    15,   402,   399,  -253,   401,    60,   404,    47,
     404,  -253,  -253,   242,  -253,  -253,  -253,   405,   407,  -253,
     409,  -253,    78,   406,   314,  -253,  -253,  -253,  -253,   420,
     370,  -253,  -253,   242,   410,  -253,   436,   416,    63,  -253,
    -253,   437,  -253,   412,  -253,  -253,   411,  -253,  -253,   413,
    -253,   415,   385,   221,   442,   262,   421,  -253,   255,  -253,
    -253,   369,   419,  -253,  -253,  -253,  -253,  -253,   450,   385,
     340,  -253,  -253,   242,   422,    33,   424,   425,   417,  -253,
     453,   426,  -253,  -253,   385,   405,  -253,   407,  -253,   215,
     428,   429,   434,   431,  -253,  -253,  -253,   385,   243,  -253,
    -253,  -253,   242,  -253,  -253,  -253,  -253,   435,   438,  -253,
    -253,   191,   337,   378,   135,  -253,  -253,   320,   432,   242,
     440,   174,  -253,   441,   339,  -253,  -253,   433,   322,   328,
    -253,   242,   333,  -253,  -253,  -253,  -253,   181,   443,  -253,
    -253,  -253,   385,   439,  -253,  -253,  -253
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   110,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    37,     0,     5,     7,     8,
      10,     6,   113,     3,     0,     0,    16,    19,   186,     0,
      44,     0,    14,    75,    76,     0,     0,    78,    46,     0,
       0,     0,     0,   112,     0,   109,     0,   168,     0,     0,
       0,   167,    14,   159,    63,    64,     0,    66,     0,    94,
      91,    65,     0,     0,     0,     0,     0,    61,    62,    59,
      60,   192,    57,    58,     0,     0,     0,     0,    70,    13,
       0,     0,     0,    79,     0,    45,     0,     0,    12,    14,
       0,     0,     0,     0,     0,     0,     0,    68,     0,     0,
       0,     0,   175,    96,     0,   175,   185,   186,    24,    18,
       0,    21,    22,    14,    53,    52,    51,   188,     0,     0,
     187,    47,     0,    48,   132,    74,    77,    85,    86,    87,
      88,     0,    89,    14,    80,    84,     0,     0,    14,    12,
      12,   110,   111,   107,   108,     0,     0,     0,   164,   166,
     165,    14,   152,   153,   151,     0,   156,   175,   149,   150,
      98,    14,     0,   174,     0,    92,   174,    93,     0,    17,
       0,     0,     0,   192,     0,     0,     0,    72,     0,    14,
      71,   110,   110,    38,   115,     0,     0,    69,     0,     0,
     175,   158,   174,     0,     0,     0,    67,   184,   182,   181,
     183,    95,    23,    20,   193,   194,    35,    15,    14,     0,
     191,   189,     0,    90,    81,     0,    83,    73,    39,    36,
     123,   121,   119,     0,   175,   117,   123,     0,   175,     0,
     175,   160,   154,   174,   155,   148,   161,   186,   100,   103,
      99,    97,    35,     0,   110,    28,    25,    49,    50,   192,
       0,    54,    82,     0,   127,   128,     0,   131,    14,   114,
     120,     0,   170,   175,   172,   174,     0,   180,   177,   175,
     179,     0,   157,     0,     0,     0,     0,    26,     0,    34,
      33,    41,     0,    30,    31,    32,   190,    55,     0,   122,
       0,   118,   129,     0,   142,     0,     0,   174,     0,   162,
     174,     0,   163,   105,   104,     0,   102,   101,    27,     0,
       0,     0,     0,     0,   124,   125,   126,   130,     0,   106,
     135,   116,     0,   171,   169,   178,   176,     0,     0,    35,
      56,     0,     0,   136,   175,    35,    35,   110,     0,     0,
       0,     0,   144,     0,     0,   138,   137,     0,   110,   110,
      42,     0,   146,   141,   134,   143,   140,     0,     0,   173,
      43,    40,   145,     0,   133,   139,   147
  };

  const short
  parser::yypgoto_[] =
  {
    -253,  -253,   454,   -83,   -50,  -240,  -253,  -253,  -253,   289,
    -253,   234,    68,  -253,  -253,  -253,  -253,  -235,   192,   196,
     209,   270,   306,  -233,  -253,  -253,   414,   468,   -72,   350,
    -146,  -231,  -253,  -253,  -253,  -253,   207,   210,  -227,  -253,
    -253,  -253,  -253,  -253,  -253,   188,   259,  -253,  -253,  -253,
     -74,  -253,  -253,   142,  -252,  -253,   295,  -253,   294,   -24,
    -253,  -253,   193,  -104,  -253,  -253,   189,  -253,  -253,    -4,
    -253,  -159,  -168
  };

  const short
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    78,    13,    27,    63,   110,   111,
     207,   243,   244,    14,    15,   280,   281,    16,    40,    41,
      30,   123,    75,    17,    18,    32,    33,    83,   133,   134,
     135,    19,   104,   105,    20,   195,   238,   239,    21,   145,
      22,    45,    46,   223,   224,   225,   254,   291,   226,   294,
      79,   319,   320,   341,   342,   157,   158,   189,   190,    60,
     228,   263,   264,   164,   230,   269,   270,   102,    61,    53,
     118,   119,   245
  };

  const short
  parser::yytable_[] =
  {
      52,   167,    97,   208,   279,   141,    31,    34,    37,   282,
     127,   283,   138,   284,   211,    28,    43,   285,   255,   121,
      24,    94,    95,    76,    25,    31,    93,   127,   128,   129,
     130,    37,   216,    74,   101,    31,   220,     1,   112,   142,
      89,    76,   131,    28,    28,   128,   129,   130,   107,   122,
     250,   132,   267,   193,    44,    35,   181,   182,   221,   256,
     252,    31,    31,   171,   179,    47,   108,    49,   132,   216,
     149,   150,    28,    34,   159,    29,   161,   222,    37,    28,
      50,   109,   251,   177,   137,    81,   234,   268,   180,   355,
     286,    51,   136,   204,   247,   261,    76,   279,    80,  -174,
     262,   187,   282,   205,   283,   355,   284,     6,   279,   279,
     285,   196,    82,   282,   282,   283,   283,   284,   284,   137,
     259,   285,   285,    74,   266,   122,   271,    94,    95,   217,
     204,    93,   191,    37,     7,    28,    54,    55,   198,   199,
     205,    23,   127,    26,   202,   206,   112,   143,    94,    95,
     333,   106,    47,    48,    49,    56,    28,    57,   246,   298,
     128,   129,   130,   343,   345,   301,   144,    58,   159,    28,
     191,    59,   265,    47,    48,    49,   358,   338,    51,    28,
     152,   153,    42,   132,   338,    28,   152,   153,    50,   188,
      65,    66,    62,   339,   338,    84,    47,    48,    49,    51,
     339,   154,    47,    48,    49,   354,   204,   154,   295,   272,
     339,   155,   364,   114,    28,   156,   205,    50,    28,    54,
      55,   156,    51,   340,    28,    88,   303,    74,    51,   289,
     347,    47,    48,    49,    86,    47,    48,    49,    64,    87,
      57,    47,    48,    49,   332,    28,    50,   197,    85,   304,
      58,   272,    91,   107,    59,    90,    50,    51,   204,   346,
      92,    51,    47,    48,    49,   237,    99,    51,   205,   317,
      47,   108,    49,   331,   115,   116,    76,    50,   100,    94,
      95,     8,    47,    48,    49,    50,     9,    76,    51,    24,
      10,    77,   103,   309,    11,    12,    51,    50,   334,    76,
     117,    94,    95,   113,    96,     8,   120,     8,    51,   183,
       9,   124,     9,   126,    10,   352,    10,   278,    11,    12,
      11,    12,     9,   278,   148,   278,    10,   362,     9,   139,
       9,   278,    10,   218,    10,   219,     9,    94,    95,   140,
      10,   146,   338,   314,   315,   -29,    94,    95,    65,    66,
     147,   350,   204,   360,   204,   151,   204,   165,   339,   361,
     148,   162,   205,   160,   205,   316,   205,   344,   363,    67,
      68,    69,    70,   242,    66,    -4,  -191,    98,     8,    38,
      39,    74,    71,     9,    72,    73,    74,    10,   169,   170,
     163,    11,    12,    67,    68,    69,    70,   337,    94,    95,
     214,   215,   166,   348,   349,   173,   287,   288,    72,    73,
     168,    76,   174,   172,   175,   184,   178,    95,   185,   186,
     192,   194,   200,   201,   210,   212,   213,   231,   227,   229,
     233,   232,   236,   241,   249,   253,   258,   277,   257,   292,
     293,   265,   296,   273,   274,   305,   275,   299,   290,   297,
     300,   302,   308,   312,   313,     5,   318,   324,   267,   203,
     261,   322,   327,   328,   329,   335,   326,   330,   336,   359,
     351,   353,   356,   310,   365,   366,   276,   311,   209,   248,
      36,   176,   307,   321,   306,   260,   357,   235,   240,   325,
     323,   125
  };

  const unsigned short
  parser::yycheck_[] =
  {
      24,   105,    52,   171,   244,    88,    10,    11,    12,   244,
       3,   244,    84,   244,   173,     3,     7,   244,     3,     5,
      34,    13,    14,    33,    38,    29,    50,     3,    21,    22,
      23,    35,   178,    43,    58,    39,     3,    32,    62,    89,
      44,    33,    35,     3,     3,    21,    22,    23,     3,    35,
       4,    44,     5,   157,    45,    43,   139,   140,    25,    44,
      36,    65,    66,   113,   136,    20,    21,    22,    44,   215,
      94,    95,     3,    77,    98,    35,   100,    44,    82,     3,
      35,    36,    36,   133,    43,    16,   190,    40,   138,   341,
     249,    46,    16,    15,     4,    35,    33,   337,    18,    36,
      40,   151,   337,    25,   337,   357,   337,     0,   348,   349,
     337,   161,    43,   348,   349,   348,   349,   348,   349,    43,
     224,   348,   349,    43,   228,    35,   230,    13,    14,   179,
      15,   155,   156,   137,     0,     3,     4,     5,   162,   163,
      25,     0,     3,     3,   168,    30,   170,     3,    13,    14,
     318,    37,    20,    21,    22,    23,     3,    25,   208,   263,
      21,    22,    23,   331,   332,   269,    22,    35,   192,     3,
     194,    39,    37,    20,    21,    22,   344,     3,    46,     3,
       4,     5,    34,    44,     3,     3,     4,     5,    35,    36,
      13,    14,    35,    19,     3,    16,    20,    21,    22,    46,
      19,    25,    20,    21,    22,    31,    15,    25,   258,   233,
      19,    35,    31,    36,     3,    39,    25,    35,     3,     4,
       5,    39,    46,    32,     3,    30,     5,    43,    46,   253,
     334,    20,    21,    22,    34,    20,    21,    22,    29,    34,
      25,    20,    21,    22,   318,     3,    35,    36,    39,   273,
      35,   275,    35,     3,    39,     9,    35,    46,    15,   333,
      35,    46,    20,    21,    22,     3,    35,    46,    25,   293,
      20,    21,    22,    30,    65,    66,    33,    35,    33,    13,
      14,     3,    20,    21,    22,    35,     8,    33,    46,    34,
      12,    37,     5,    38,    16,    17,    46,    35,   322,    33,
       4,    13,    14,    34,    38,     3,     3,     3,    46,    31,
       8,     3,     8,     3,    12,   339,    12,     3,    16,    17,
      16,    17,     8,     3,    36,     3,    12,   351,     8,    30,
       8,     3,    12,    31,    12,    31,     8,    13,    14,    30,
      12,     5,     3,     3,     4,    31,    13,    14,    13,    14,
       5,    31,    15,    31,    15,    25,    15,    40,    19,    31,
      36,    37,    25,     5,    25,    25,    25,    30,    35,    26,
      27,    28,    29,    32,    14,     0,    34,    39,     3,    10,
      11,    43,    39,     8,    41,    42,    43,    12,    36,    37,
      37,    16,    17,    26,    27,    28,    29,   329,    13,    14,
      36,    37,    37,   335,   336,    34,    36,    37,    41,    42,
      38,    33,     4,    40,    18,    35,    37,    14,    37,    37,
      37,    37,    36,     5,     4,    37,     3,    40,    39,    39,
      37,    40,    40,    36,    34,    34,    37,    31,    36,     3,
      24,    37,     5,    38,    37,     3,    37,    36,    38,    37,
      37,    36,    31,    34,     4,     1,    34,    40,     5,   170,
      35,    37,    34,    34,    30,    30,    40,    36,    30,    36,
      38,    31,    31,   281,    31,    36,   242,   281,   172,   209,
      12,   131,   275,   295,   274,   226,   344,   192,   194,   300,
     297,    77
  };

  const unsigned char
  parser::yystos_[] =
  {
       0,    32,    48,    49,    50,    49,     0,     0,     3,     8,
      12,    16,    17,    52,    60,    61,    64,    70,    71,    78,
      81,    85,    87,     0,    34,    38,     3,    53,     3,    35,
      67,   116,    72,    73,   116,    43,    74,   116,    10,    11,
      65,    66,    34,     7,    45,    88,    89,    20,    21,    22,
      35,    46,   106,   116,     4,     5,    23,    25,    35,    39,
     106,   115,    35,    54,    67,    13,    14,    26,    27,    28,
      29,    39,    41,    42,    43,    69,    33,    37,    51,    97,
      18,    16,    43,    74,    16,    67,    34,    34,    30,   116,
       9,    35,    35,   106,    13,    14,    38,    51,    39,    35,
      33,   106,   114,     5,    79,    80,    37,     3,    21,    36,
      55,    56,   106,    34,    36,    67,    67,     4,   117,   118,
       3,     5,    35,    68,     3,    73,     3,     3,    21,    22,
      23,    35,    44,    75,    76,    77,    16,    43,    75,    30,
      30,    50,    51,     3,    22,    86,     5,     5,    36,   106,
     106,    25,     4,     5,    25,    35,    39,   102,   103,   106,
       5,   106,    37,    37,   110,    40,    37,   110,    38,    36,
      37,    51,    40,    34,     4,    18,    76,    51,    37,    75,
      51,    50,    50,    31,    35,    37,    37,    51,    36,   104,
     105,   106,    37,   110,    37,    82,    51,    36,   106,   106,
      36,     5,   106,    56,    15,    25,    30,    57,   119,    69,
       4,   118,    37,     3,    36,    37,    77,    51,    31,    31,
       3,    25,    44,    90,    91,    92,    95,    39,   107,    39,
     111,    40,    40,    37,   110,   103,    40,     3,    83,    84,
     105,    36,    32,    58,    59,   119,    51,     4,    68,    34,
       4,    36,    36,    34,    93,     3,    44,    36,    37,   110,
      93,    35,    40,   108,   109,    37,   110,     5,    40,   112,
     113,   110,   106,    38,    37,    37,    58,    31,     3,    52,
      62,    63,    64,    70,    78,    85,   118,    36,    37,   106,
      38,    94,     3,    24,    96,    51,     5,    37,   110,    36,
      37,   110,    36,     5,   106,     3,    84,    83,    31,    38,
      65,    66,    34,     4,     3,     4,    25,   106,    34,    98,
      99,    92,    37,   109,    40,   113,    40,    34,    34,    30,
      36,    30,    97,   119,   106,    30,    30,    59,     3,    19,
      32,   100,   101,   119,    30,   119,    97,   110,    59,    59,
      31,    38,   106,    31,    31,   101,    31,   100,   119,    36,
      31,    31,   106,    35,    31,    31,    36
  };

  const unsigned char
  parser::yyr1_[] =
  {
       0,    47,    48,    48,    49,    50,    50,    50,    50,    50,
      50,    50,    50,    51,    51,    52,    53,    54,    54,    54,
      55,    55,    56,    56,    56,    57,    57,    57,    58,    58,
      59,    59,    59,    59,    59,    59,    60,    60,    61,    61,
      62,    62,    63,    63,    64,    65,    66,    67,    67,    67,
      67,    67,    67,    67,    68,    68,    68,    69,    69,    69,
      69,    69,    69,    70,    70,    70,    70,    70,    70,    70,
      71,    71,    71,    71,    72,    72,    73,    73,    74,    74,
      75,    75,    75,    76,    76,    77,    77,    77,    77,    77,
      77,    78,    78,    79,    79,    80,    80,    81,    82,    82,
      82,    82,    83,    83,    84,    84,    85,    86,    86,    87,
      87,    88,    89,    89,    90,    90,    91,    91,    92,    92,
      92,    92,    93,    93,    94,    94,    94,    94,    95,    95,
      96,    96,    97,    98,    98,    98,    99,    99,    99,    99,
      99,    99,    99,   100,   100,   101,   101,   101,   102,   102,
     103,   103,   103,   103,   103,   104,   104,   105,   105,   106,
     106,   106,   106,   106,   106,   106,   106,   106,   106,   107,
     107,   108,   108,   109,   110,   110,   111,   111,   112,   112,
     113,   114,   114,   115,   115,   115,   116,   116,   117,   117,
     117,   118,   118,   119,   119
  };

  const unsigned char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     6,     1,     3,     2,     0,
       3,     1,     1,     3,     1,     2,     3,     4,     1,     1,
       2,     2,     2,     2,     2,     0,     6,     1,     5,     6,
       6,     1,     5,     6,     2,     2,     1,     3,     3,     6,
       6,     3,     3,     3,     4,     5,     7,     1,     1,     1,
       1,     1,     1,     3,     3,     3,     3,     6,     4,     6,
       3,     5,     5,     6,     3,     1,     1,     3,     1,     2,
       1,     3,     4,     3,     1,     1,     1,     1,     1,     1,
       3,     3,     5,     2,     0,     3,     1,     7,     0,     2,
       2,     4,     3,     1,     3,     3,     9,     1,     1,     2,
       0,     3,     1,     0,     2,     0,     4,     1,     3,     1,
       2,     1,     2,     0,     2,     2,     2,     0,     2,     3,
       2,     0,     2,     5,     4,     1,     2,     3,     3,     5,
       4,     4,     0,     2,     1,     3,     2,     4,     3,     1,
       1,     1,     1,     1,     3,     2,     0,     3,     1,     1,
       5,     5,     7,     7,     3,     3,     3,     1,     1,     4,
       2,     3,     1,     6,     1,     0,     4,     2,     3,     1,
       1,     3,     3,     4,     4,     2,     1,     3,     1,     3,
       5,     1,     0,     1,     1
  };



  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a yyntokens_, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "$undefined", "NAME", "NUMBER", "STRING",
  "LEXERROR", "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF", "OR", "AND",
  "PASS", "IMPORT", "FROM", "AS", "RAISE", "NOTHING", "NAMEDTUPLE",
  "COLL_NAMEDTUPLE", "TYPEVAR", "ARROW", "ELLIPSIS", "EQ", "NE", "LE",
  "GE", "INDENT", "DEDENT", "TRIPLEQUOTED", "TYPECOMMENT", "':'", "'('",
  "')'", "','", "'='", "'['", "']'", "'<'", "'>'", "'.'", "'*'", "'@'",
  "'?'", "$accept", "start", "unit", "alldefs", "maybe_type_ignore",
  "classdef", "class_name", "parents", "parent_list", "parent",
  "maybe_class_funcs", "class_funcs", "funcdefs", "if_stmt",
  "if_and_elifs", "class_if_stmt", "class_if_and_elifs", "if_cond",
  "elif_cond", "else_cond", "condition", "version_tuple", "condition_op",
  "constantdef", "importdef", "import_items", "import_item", "import_name",
  "from_list", "from_items", "from_item", "alias_or_constant",
  "maybe_string_list", "string_list", "typevardef", "typevar_args",
  "typevar_kwargs", "typevar_kwarg", "funcdef", "funcname", "decorators",
  "decorator", "maybe_async", "params", "param_list", "param",
  "param_type", "param_default", "param_star_name", "return", "typeignore",
  "maybe_body", "empty_body", "body", "body_stmt", "type_parameters",
  "type_parameter", "maybe_type_list", "type_list", "type",
  "named_tuple_fields", "named_tuple_field_list", "named_tuple_field",
  "maybe_comma", "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "type_tuple_elements", "type_tuple_literal",
  "dotted_name", "getitem_key", "maybe_number", "pass_or_ellipsis", YY_NULLPTR
  };

#if PYTYPEDEBUG
  const unsigned short
  parser::yyrline_[] =
  {
       0,   134,   134,   135,   139,   143,   144,   145,   146,   152,
     153,   154,   159,   163,   164,   171,   178,   189,   190,   191,
     195,   196,   200,   201,   202,   206,   207,   208,   212,   213,
     217,   218,   223,   224,   229,   230,   235,   238,   243,   247,
     266,   269,   274,   278,   290,   294,   298,   302,   305,   308,
     311,   314,   315,   316,   321,   322,   323,   329,   330,   331,
     332,   333,   334,   338,   342,   346,   350,   354,   358,   362,
     369,   373,   377,   383,   392,   393,   397,   398,   403,   404,
     411,   412,   413,   417,   418,   422,   423,   426,   429,   432,
     435,   439,   440,   444,   445,   449,   450,   454,   461,   462,
     463,   464,   468,   469,   473,   475,   479,   496,   497,   501,
     502,   506,   510,   511,   515,   516,   528,   529,   533,   534,
     535,   536,   540,   541,   545,   546,   547,   548,   552,   553,
     557,   558,   562,   566,   567,   568,   572,   573,   574,   575,
     576,   577,   578,   582,   583,   587,   588,   589,   593,   594,
     598,   599,   601,   602,   604,   611,   612,   616,   617,   621,
     625,   629,   633,   637,   641,   642,   643,   644,   645,   649,
     650,   654,   655,   659,   663,   664,   668,   669,   673,   676,
     680,   687,   688,   697,   702,   708,   715,   716,   730,   731,
     736,   744,   745,   749,   750
  };

  // Print the state stack on the debug stream.
  void
  parser::yystack_print_ ()
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << i->state;
    *yycdebug_ << '\n';
  }

  // Report on the debug stream that the rule \a yyrule is going to be reduced.
  void
  parser::yy_reduce_print_ (int yyrule)
  {
    unsigned yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):\n";
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  parser::token_number_type
  parser::yytranslate_ (int t)
  {
    // YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to
    // TOKEN-NUM as returned by yylex.
    static
    const token_number_type
    translate_table[] =
    {
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      35,    36,    44,     2,    37,     2,    43,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    34,     2,
      41,    38,    42,    46,    45,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    39,     2,    40,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33
    };
    const unsigned user_token_number_max_ = 288;
    const token_number_type undef_token_ = 2;

    if (static_cast<int> (t) <= yyeof_)
      return yyeof_;
    else if (static_cast<unsigned> (t) <= user_token_number_max_)
      return translate_table[t];
    else
      return undef_token_;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1242
} // pytype
#line 3046 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:1242
#line 753 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1243


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
