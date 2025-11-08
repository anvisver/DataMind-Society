from __future__ import annotations
from enum import Enum
import ast
__all__ = ["dat", "dat_support", "Maths_Support","AC","BC", "EpochType"]

class EpochType(Enum):
    """Enum representing era/epoch for dat objects. Members: AC ('ac') and BC ('bc'). Used to mark whether a dat's rawtime is positive (AC) or negative (BC)."""
    AC = "ac"  # After Christ (default)
    BC = "bc"  # Before Christ

AC = EpochType.AC
"""Alias for EpochType.AC exported for convenient external usage."""

BC = EpochType.BC
"""Alias for EpochType.BC exported for convenient external usage."""


class Maths_Support:
    """Mixin-like utility class that stores a numeric `rawtime` (seconds) and implements arithmetic and comparison dunder methods operating on that rawtime. Designed so dat objects can perform intuitive math (addition, subtraction, scaling, comparisons) based on seconds. It stores `rawtime` as a float and delegates creation of result objects to dat.operand when returning dat instances."""
    
    def __init__(self, rawtime:float) -> dat:
        """Initialize a Maths_Support instance with a numeric `rawtime`. Side-effect: stores `self.rawtime` (float)."""
        self.rawtime = rawtime

    def __add__(self, other) -> dat:
        """Add either another Maths_Support (adds their rawtime) or a numeric scalar (seconds). Returns a new dat via dat.operand(sum). Raises TypeError for unsupported types (code currently marks unsupported branches)."""
        if isinstance(other, Maths_Support):
            return dat.operand(self.rawtime + other.rawtime)
        elif isinstance(other, (int, float)):
            return dat.operand(self.rawtime + other)

    def __sub__(self, other) -> dat:
        """Subtract another Maths_Support's rawtime or a numeric scalar from this instance's rawtime. Returns a new dat via dat.operand(difference). Unsupported types are intended to raise an error (placeholder in code)."""
        if isinstance(other, Maths_Support):
            return dat.operand(self.rawtime - other.rawtime)
        elif isinstance(other, (int, float)):
            return dat.operand(self.rawtime - other)

    def __mul__(self, other) -> dat:
        """Multiply this instance's rawtime by another Maths_Support.rawtime or a numeric scalar. Returns a new dat via dat.operand(product). Unsupported types are not handled in the code and should result in an error."""
        if isinstance(other, Maths_Support):
            return dat.operand(self.rawtime * other.rawtime)
        elif isinstance(other, (int, float)):
            return dat.operand(self.rawtime * other)

    def __truediv__(self, other) -> dat:
        """True-divide this instance's rawtime by another Maths_Support.rawtime or a numeric scalar and return a new dat via dat.operand(quotient). Division by zero and unsupported types are not explicitly handled in the code and should be guarded by callers."""
        if isinstance(other, Maths_Support):
            return dat.operand(self.rawtime / other.rawtime)
        elif isinstance(other, (int, float)):
            return dat.operand(self.rawtime / other)

    def __floordiv__(self, other) -> dat:
        """Floor-divide this instance's rawtime by another Maths_Support.rawtime or a numeric scalar, returning a new dat produced by dat.operand(floor_result). Unsupported types are marked in the code with placeholders."""
        if isinstance(other, Maths_Support):
            return dat.operand(self.rawtime // other.rawtime)
        elif isinstance(other, (int, float)):
            return dat.operand(self.rawtime // other)

    def __mod__(self, other) -> dat:
        """Return the remainder of dividing this instance's rawtime by another Maths_Support.rawtime or a numeric scalar. Unlike other arithmetic dunders, this method returns a plain numeric remainder (float) rather than a dat object. Unsupported types are left as placeholders."""
        if isinstance(other, Maths_Support):
            return self.rawtime % other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime % other

    def __pow__(self, other) -> dat:
        """Raise this instance's rawtime to the power of another Maths_Support.rawtime or numeric scalar, returning a new dat via dat.operand(result). Unsupported types are marked as TODO in the code."""
        if isinstance(other, Maths_Support):
            return dat.operand(self.rawtime ** other.rawtime)
        elif isinstance(other, (int, float)):
            return dat.operand(self.rawtime ** other)

    def __eq__(self, other) -> dat:
        """Equality comparison between this instance's rawtime and a Maths_Support.rawtime or numeric scalar; returns a boolean."""
        if isinstance(other, Maths_Support):
            return self.rawtime == other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime == other

    def __gt__(self, other) -> dat:
        """Greater-than comparison against another Maths_Support or numeric scalar; returns a boolean."""
        if isinstance(other, Maths_Support):
            return self.rawtime > other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime > other

    def __ge__(self, other) -> dat:
        """Greater-than-or-equal comparison against another Maths_Support or numeric scalar; returns a boolean."""
        if isinstance(other, Maths_Support):
            return self.rawtime >= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime >= other

    def __lt__(self, other) -> dat:
        """Less-than comparison against another Maths_Support or numeric scalar; returns a boolean."""
        if isinstance(other, Maths_Support):
            return self.rawtime < other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime < other

    def __le__(self, other) -> dat:
        """Less-than-or-equal comparison against another Maths_Support or numeric scalar; returns a boolean."""
        if isinstance(other, Maths_Support):
            return self.rawtime <= other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime <= other

    def __ne__(self, other) -> dat:
        """Inequality comparison against another Maths_Support or numeric scalar; returns a boolean."""
        if isinstance(other, Maths_Support):
            return self.rawtime != other.rawtime
        elif isinstance(other, (int, float)):
            return self.rawtime != other

class dat_support:
    """Mixin providing high-level property views and conversion helpers for dat instances. Exposes many convenient read-only properties (year, month, day, hour, minute, second, time, date) that behave differently depending on the `converter` mode: 0 -> return raw stored components, 1 -> convert from `rawtime` (seconds) to the requested unit, 2 -> return `dat.datetime` objects constructed from stored components. Also holds `data`, `source` and a `converter` flag which are populated from the dat's `output` during initialization."""

    def __init__(self):
        """Initialize dat_support by reading `self.output` and setting `self.data` (component list) and `self.source` (string describing which view), and set `self.converter` to 0. Expects `self.output` to be populated by dat before calling."""
        self.data = self.output [0]
        self.source = self.output[1]
        self.converter = 0

    @property
    def _convert_to_(self):
        """Property that sets `self.converter = 1` and returns self. When used before a numeric property it switches the behavior to 'convert from rawtime to unit' mode."""
        self.converter = 1
        return self

    @property
    def _object_only_accounts_for_(self):
        """Property that sets `self.converter = 2` and returns self. When used before a property it makes that property return a dat.datetime object built from the underlying components."""
        self.converter = 2
        return self

    @property
    def year(self) -> dat | float | int:
        """Property returning the year. Behavior depends on converter: converter==1 -> returns exact years computed from `rawtime` (float, accounts for leap years); converter==2 -> returns dat.datetime([year]) (a dat instance representing the year); else returns the stored data component as float."""
        def is_leap_year(year):
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        def seconds_in_year(year):
            days = 366 if is_leap_year(year) else 365
            return days * 24 * 60 * 60
        def seconds_to_exact_years(seconds):
            years_passed = 0
            year = 0
            while seconds >= seconds_in_year(year):
                seconds -= seconds_in_year(year)
                year += 1
                years_passed += 1
            fraction_of_year:float | int = seconds / seconds_in_year(year)
            total_years = years_passed + fraction_of_year
            return total_years
        if self.converter == 1:
            return seconds_to_exact_years(self.rawtime)
        elif self.converter == 2:
            return dat.datetime([self.data[0]])
        return float(self.data[0])

    @property  
    def month(self) -> dat | float | int:
        """Property returning the month. converter==1 -> returns months as fractional months derived from `rawtime` (accounts for month lengths and leap years); converter==2 -> returns dat.datetime([1, month]); else returns stored month component as float."""
        def is_leap_year(year):
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        def days_in_month(year, month):
            if month in {1, 3, 5, 7, 8, 10, 12}:
                return 31
            elif month in {4, 6, 9, 11}:
                return 30
            elif month == 2:
                return 29 if is_leap_year(year) else 28
            else:
                raise ValueError("Month must be 1..12")
        def seconds_in_month(year, month):
            return days_in_month(year, month) * 24 * 60 * 60
        def seconds_to_exact_months(seconds):
            year, month = 0, 1
            months_passed = 0
            while seconds >= seconds_in_month(year, month):
                seconds -= seconds_in_month(year, month)
                months_passed += 1
                month += 1
                if month > 12:
                    month = 1
                    year += 1
            fraction_of_month = seconds / seconds_in_month(year, month)
            total_months = months_passed + fraction_of_month
            return total_months 
        if self.converter == 1:
            return seconds_to_exact_months(self.rawtime)
        elif self.converter == 2:
            return dat.datetime([1,self.data[1]])
        return float(self.data[1])

    @property
    def day(self) ->dat | float | int:
        """Property returning the day. converter==1 -> returns days derived from `rawtime` (seconds -> days); converter==2 -> returns dat.datetime([0,0,day]); else returns stored day component as float."""
        def seconds_to_days(seconds: float) -> float:
            SECONDS_PER_DAY = 24 * 60 * 60
            return seconds / SECONDS_PER_DAY
        if self.converter == 1:
            return seconds_to_days(self.rawtime)
        elif self.converter == 2:
            return dat.datetime([0,0,self.data[2]])
        return float(self.data[2])

    @property
    def hour(self) ->dat | float | int:
        """Property returning the hour. converter==1 -> returns hours computed from `rawtime` (rawtime/3600); converter==2 -> returns dat.datetime([1,1,1,hour]); else returns stored hour component as float."""
        if self.converter == 1:
            return self.rawtime/3600
        if self.converter == 2:
            return dat.datetime([1,1,1,self.data[3]])
        return float(self.data[3])

    @property
    def minute(self) ->dat | float | int:
        """Property returning the minute. converter==1 -> returns minutes from `rawtime` (rawtime/60); converter==2 -> returns dat.datetime([1,1,1,0,minute]); else returns stored minute component as float."""
        if self.converter == 1:
            return self.rawtime / 60
        elif self.converter == 2:
            return dat.datetime([1,1,1,0,self.data[4]])
        return float(self.data[4])

    @property
    def second(self) ->dat | float | int:
        """Property returning the second. converter==1 -> returns seconds (rawtime); converter==2 -> returns dat.datetime([1,1,1,0,0,second]); else returns stored second component as float."""
        if self.converter == 1:
            return self.rawtime
        elif self.converter == 2:
            return dat.datetime([1,1,1,0,0,self.data[5]])
        return float(self.data[5])

    @property
    def time(self) -> dat | list[int | float] | float | int:
        """Property returning a time view: converter==1 -> returns hour * minute * second (product of those conversions — note this behavior is unusual and likely not what most users expect); converter==2 -> returns dat.datetime built from full time components; else returns first three stored components (`data[0:3]`)."""
        if self.converter == 1:
            return self.hour*self.minute*self.second
        elif self.converter == 2:
            return dat.datetime([1,1,1,self.data[3],self.data[4],self.data[5]])
        return self.data[0:3]

    @property
    def date(self) -> dat | list[int] | float | int:
        """Property returning a date view: converter==1 -> returns year * month * day (product — again nonstandard and should be used with care); converter==2 -> returns dat.datetime built from date components; else returns stored date slice (`data[3:6]`)."""
        if self.converter == 1:
            return self.year*self.month*self.day
        elif self.converter == 2:
            return dat.datetime([self.data[0],self.data[1],self.data[2]])
        return self.data[3:6]

class dat(Maths_Support,dat_support):
    """
    =====================================================================
    OVERVIEW — what a `dat` is and the design ideas
    =====================================================================

    A `dat` object is a custom date/time representation built around a single canonical internal value called `rawtime`.  
    - **`rawtime`**: a floating-point number representing a number of seconds relative to a chosen epoch (the library’s epoch is “year 0, month 1, day 1, 00:00:00” by convention). Positive `rawtime` values are considered AC (After Christ), negative values are BC (Before Christ).  
    - `dat` combines numeric arithmetic (via `Maths_Support`) with rich component access and conversion helpers (via `dat_support`). The object also stores:
    - `drift`: an offset in seconds that can be used to shift or correct time representation.
    - `template`: an ordering/definition of which input fields were provided.
    - `output`: a 2-element list `[parts, source]` where `parts` is `[Y,M,D,h,mi,s]` and `source` is a string describing the origin of those parts (e.g., "fulldat", "date", "time", etc.).
    - `epoch_type`: either `AC` or `BC`, derived from `rawtime`.
    - `min_clock_value`: a 3-item list [min_year, min_month, min_day] used when normalizing values to enforce lower bounds.

    Philosophy: store time as seconds for precise arithmetic, but expose human-friendly component access and robust conversion routines that account for leap years, varying month lengths, fractional fields, and carry/borrowing across units.

    =====================================================================
    KEY CONSTANTS / STATIC DATA
    =====================================================================

    - `TIME_UNITS`: mapping of unit tokens to seconds. Special note: the `"m"` value is itself a dictionary mapping month index -> seconds (so month length depends on month index), while `"y"` is an approximate seconds-per-year value (31536000).
    - `_SENTINEL_VALUE_`: a unique sentinel object used to detect when `input_compiler` should parse a compact serialized string format.
    - `CENTRAL_EUROPEAN_TIMELINE`: numeric constant `7200` (seconds) intended for CET timezone or similar drift usage.
    - `EpochType` (`AC`, `BC`): Enum naming for era/epoch. `AC` and `BC` are also exported as convenience names.

    =====================================================================
    MATHS_SUPPORT — behavior and returned types
    =====================================================================

    `Maths_Support` is a mixin that stores `self.rawtime` and implements arithmetic and comparison dunder methods:

    - Arithmetic methods: `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__pow__`
    - Accept either another `Maths_Support` (commonly another `dat`) or a numeric scalar (`int`/`float`).
    - When operating with another `Maths_Support`, these methods use `other.rawtime`.
    - **Return value**: Most arithmetic operations return a **new `dat`** instance created by calling `dat.operand(<result_raw_seconds>)`. This wraps the numeric result back into a `dat` object.
    - Special-case: `__mod__` returns a numeric remainder (`float`) rather than a `dat` (this is intended for periodic measures).  
    - Edge cases not fully handled in code: unsupported types and division by zero are not explicitly guarded — they’re annotated in the source as places where an error should be raised.

    - Comparison methods: `__eq__`, `__ne__`, `__gt__`, `__ge__`, `__lt__`, `__le__`
    - Compare `self.rawtime` to `other.rawtime` (if `other` is `Maths_Support`) or to numeric scalars.
    - **Return**: boolean.

    Recommended usage: use arithmetic between `dat` objects or between a `dat` and a numeric seconds value, then use result `dat` methods or properties to read human-friendly components.

    =====================================================================
    dat_support — view properties and converter modes
    =====================================================================

    `dat_support` provides property accessors which expose the `output` components (Y, M, D, h, mi, s) in different modes depending on `self.converter`.

    - Initialization: `dat_support.__init__` expects that `self.output` is already set (by `dat`) and sets:
    - `self.data` = `self.output[0]` (the `[Y,M,D,h,mi,s]` list)
    - `self.source` = `self.output[1]` (a string describing the origin/view)
    - `self.converter = 0` by default.

    - Two configuration properties switch the conversion mode:
    - `_convert_to_` (property): sets `self.converter = 1` and returns `self`. When used before reading a property it switches that property to convert *from* `rawtime` into the requested unit (rather than returning stored components).
    - `_object_only_accounts_for_` (property): sets `self.converter = 2` and returns `self`. In this mode, many properties return a `dat.datetime(...)` instance constructed from component or partial component values (i.e., they return `dat` objects rather than raw floats/ints).

    - Provided properties:
    - `year`, `month`, `day`, `hour`, `minute`, `second`
        - Default (`converter == 0`): return the stored `self.data[n]` piece as a `float`.
        - If `converter == 1`: convert using `rawtime` into the requested unit.
        - If `converter == 2`: return a `dat` object built from the relevant components.
    - `time` and `date`
        - Default returns slices of `self.data`.
        - If `converter == 1`, `time` returns `hour * minute * second` and `date` returns `year * month * day`. (Unusual behavior.)
        - If `converter == 2`, they construct `dat.datetime(...)` objects from the relevant slices.

    =====================================================================
    `dat` class — construction, factories, and serialization
    =====================================================================

    Primary construction patterns:

    1. **`dat()`** — default constructor, placeholder object.
    2. **`dat.operand(base_rawtime, *, drift=0, reverse=False, min_clock_value=[1,1,1])`** — create from seconds.
    3. **`dat.stamp(input_value, input_template=..., epoch_type=AC, *, drift=0, min_clock_value=[1,1,1])`** — partial stamping.
    4. **`dat.datetime(input_value=[0,1,1,0,0,0], epoch_type=AC, *, drift=0, template_reverse=False, min_clock_value=[1,1,1])`** — full canonical construction.
    5. **`dat.current_time(*, drift=0)`** — current local time.
    6. **`dat.input_compiler(...)`** — flexible parsing or deserialization from string.
    7. **`dat.export_compiler`** — serializes the `dat` instance.

    =====================================================================
    Normalization and conversion internals
    =====================================================================

    - `finalize_full_dat(value: list[int], epoch_type=AC, output_type="fulldat")` — normalizes components and sets `rawtime`.
    - `normalize_full(full: dict[str,float])` — carries fractional units, accounts for leap years/month lengths, enforces min_clock_value.
    - `convert_input_to_rawtime(template_value_diccionary: dict) -> float` — converts normalized fields into seconds.
    - `convert_rawtime_to_date(seconds: float | int) -> list` — inverts seconds back to `[Y,M,D,h,i,s]`.
    - `drift_converter(drift)` — unifies drift argument into float seconds.

    =====================================================================
    Parsing helper: value_template_extractor
    =====================================================================

    Flexible input parsing of `value` and `template` for stamps and datetime constructors.

    =====================================================================
    String formatting and output
    =====================================================================

    - `self.output` stores `[parts, source]`.
    - `__str__` produces human-readable representations based on `source` and `epoch_type`.

    =====================================================================
    Recommended usage patterns
    =====================================================================

    1. Create from explicit components.
    2. Create directly from seconds.
    3. Get current time.
    4. Arithmetic and comparisons.
    5. Read components vs convert from rawtime.
    6. Serialization round-trip.

    =====================================================================
    Implementation notes & quirks
    =====================================================================

    - Drift semantics, epoch handling, unimplemented error handling, unusual multiplicative behavior for `time`/`date` in converter==1, parsing fragility, month-year approximations, min_clock_value enforcement.

    =====================================================================
    Advanced notes & extensions
    =====================================================================

    - Validation, fix `time`/`date` behavior, preserve drift in arithmetic, timezone handling, better template parsing, string formatting enhancements.

    =====================================================================
    Summary / Quick Reference
    =====================================================================

    - Store: `rawtime` + `output`
    - Create: `datetime`, `stamp`, `operand`, `current_time`
    - Inspect: component properties, `_convert_to_`, `_object_only_accounts_for_`
    - Arithmetic: `+ - * / // **`, comparisons
    - Normalization: `normalize_full` handles fractional units and leap years.
    =====================================================================
    OVERVIEW — what a `dat` is and the design ideas
    =====================================================================

    A `dat` object is a custom date/time representation built around a single canonical internal value called `rawtime`.  
    - **`rawtime`**: a floating-point number representing a number of seconds relative to a chosen epoch (the library’s epoch is “year 0, month 1, day 1, 00:00:00” by convention). Positive `rawtime` values are considered AC (After Christ), negative values are BC (Before Christ).  
    - `dat` combines numeric arithmetic (via `Maths_Support`) with rich component access and conversion helpers (via `dat_support`). The object also stores:
    - `drift`: an offset in seconds that can be used to shift or correct time representation.
    - `template`: an ordering/definition of which input fields were provided.
    - `output`: a 2-element list `[parts, source]` where `parts` is `[Y,M,D,h,mi,s]` and `source` is a string describing the origin of those parts (e.g., "fulldat", "date", "time", etc.).
    - `epoch_type`: either `AC` or `BC`, derived from `rawtime`.
    - `min_clock_value`: a 3-item list [min_year, min_month, min_day] used when normalizing values to enforce lower bounds.

    Philosophy: store time as seconds for precise arithmetic, but expose human-friendly component access and robust conversion routines that account for leap years, varying month lengths, fractional fields, and carry/borrowing across units.

    =====================================================================
    KEY CONSTANTS / STATIC DATA
    =====================================================================

    - `TIME_UNITS`: mapping of unit tokens to seconds. Special note: the "m" value is itself a dictionary mapping month index -> seconds (so month length depends on month index), while "y" is an approximate seconds-per-year value (31536000).
    - `_SENTINEL_VALUE_`: a unique sentinel object used to detect when `input_compiler` should parse a compact serialized string format.
    - `CENTRAL_EUROPEAN_TIMELINE`: numeric constant 7200 (seconds) intended for CET timezone or similar drift usage.
    - `EpochType` (`AC`, `BC`): Enum naming for era/epoch. `AC` and `BC` are also exported as convenience names.

    =====================================================================
    MATHS_SUPPORT — behavior and returned types
    =====================================================================

    `Maths_Support` is a mixin that stores `self.rawtime` and implements arithmetic and comparison dunder methods:

    - Arithmetic methods: `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__pow__`
    - Accept either another `Maths_Support` (commonly another `dat`) or a numeric scalar (`int`/`float`).
    - When operating with another `Maths_Support`, these methods use `other.rawtime`.
    - **Return value**: Most arithmetic operations return a **new `dat`** instance created by calling `dat.operand(<result_raw_seconds>)`. This wraps the numeric result back into a `dat` object.
    - Special-case: `__mod__` returns a numeric remainder (`float`) rather than a `dat` (this is intended for periodic measures).  
    - Edge cases not fully handled in code: unsupported types and division by zero are not explicitly guarded — they’re annotated in the source as places where an error should be raised.

    - Comparison methods: `__eq__`, `__ne__`, `__gt__`, `__ge__`, `__lt__`, `__le__`
    - Compare `self.rawtime` to `other.rawtime` (if `other` is `Maths_Support`) or to numeric scalars.
    - **Return**: boolean.

    Recommended usage: use arithmetic between `dat` objects or between a `dat` and a numeric seconds value, then use result `dat` methods or properties to read human-friendly components.

    =====================================================================
    dat_support — view properties and converter modes
    =====================================================================

    `dat_support` provides property accessors which expose the `output` components (Y, M, D, h, mi, s) in different modes depending on `self.converter`.

    - Initialization: `dat_support.__init__` expects that `self.output` is already set (by `dat`) and sets:
    - `self.data` = `self.output[0]` (the `[Y,M,D,h,mi,s]` list)
    - `self.source` = `self.output[1]` (a string describing the origin/view)
    - `self.converter = 0` by default.

    - Two configuration properties switch the conversion mode:
    - `_convert_to_` (property): sets `self.converter = 1` and returns `self`. When used before reading a property it switches that property to convert *from* `rawtime` into the requested unit (rather than returning stored components).
    - `_object_only_accounts_for_` (property): sets `self.converter = 2` and returns `self`. In this mode, many properties return a `dat.datetime(...)` instance constructed from component or partial component values (i.e., they return `dat` objects rather than raw floats/ints).

    - Provided properties:
    - `year`, `month`, `day`, `hour`, `minute`, `second`
        - Default (`converter == 0`): return the stored `self.data[n]` piece as a `float`.
        - If `converter == 1`: convert using `rawtime` into the requested unit.
        - If `converter == 2`: return a `dat` object built from the relevant components.
    - `time` and `date`
        - Default returns slices of `self.data`.
        - If `converter == 1`, `time` returns `hour * minute * second` and `date` returns `year * month * day`. (Unusual behavior.)
        - If `converter == 2`, they construct `dat.datetime(...)` objects from the relevant slices.

    =====================================================================
    dat class — construction, factories, and serialization
    =====================================================================

    Primary construction patterns:

    1. **dat()** — default constructor, placeholder object.
    2. **dat.operand(base_rawtime, *, drift=0, reverse=False, min_clock_value=[1,1,1])** — create from seconds.
    3. **dat.stamp(input_value, input_template=..., epoch_type=AC, *, drift=0, min_clock_value=[1,1,1])** — partial stamping.
    4. **dat.datetime(input_value=[0,1,1,0,0,0], epoch_type=AC, *, drift=0, template_reverse=False, min_clock_value=[1,1,1])** — full canonical construction.
    5. **dat.current_time(*, drift=0)** — current local time.
    6. **dat.input_compiler(...)** — flexible parsing or deserialization from string.
    7. **dat.export_compiler** — serializes the dat instance.

    =====================================================================
    Normalization and conversion internals
    =====================================================================

    - `finalize_full_dat(value: list[int], epoch_type=AC, output_type="fulldat")` — normalizes components and sets `rawtime`.
    - `normalize_full(full: dict[str,float])` — carries fractional units, accounts for leap years/month lengths, enforces min_clock_value.
    - `convert_input_to_rawtime(template_value_diccionary: dict) -> float` — converts normalized fields into seconds.
    - `convert_rawtime_to_date(seconds: float | int) -> list` — inverts seconds back to `[Y,M,D,h,i,s]`.
    - `drift_converter(drift)` — unifies drift argument into float seconds.

    =====================================================================
    Parsing helper: value_template_extractor
    =====================================================================

    Flexible input parsing of `value` and `template` for stamps and datetime constructors.

    =====================================================================
    String formatting and output
    =====================================================================

    - `self.output` stores `[parts, source]`.
    - `__str__` produces human-readable representations based on `source` and `epoch_type`.

    =====================================================================
    Recommended usage patterns
    =====================================================================

    1. Create from explicit components.
    2. Create directly from seconds.
    3. Get current time.
    4. Arithmetic and comparisons.
    5. Read components vs convert from rawtime.
    6. Serialization round-trip.

    =====================================================================
    Implementation notes & quirks
    =====================================================================

    - Drift semantics, epoch handling, unimplemented error handling, unusual multiplicative behavior for `time`/`date` in converter==1, parsing fragility, month-year approximations, min_clock_value enforcement.

    =====================================================================
    Advanced notes & extensions
    =====================================================================

    - Validation, fix `time`/`date` behavior, preserve drift in arithmetic, timezone handling, better template parsing, string formatting enhancements.

    =====================================================================
    Summary / Quick Reference
    =====================================================================

    - Store: `rawtime` + `output`
    - Create: `datetime`, `stamp`, `operand`, `current_time`
    - Inspect: component properties, `_convert_to_`, `_object_only_accounts_for_`
    - Arithmetic: `+ - * / // **`, comparisons
    - Normalization: `normalize_full` handles fractional units and leap years.
    """




    TIME_UNITS:dict[str,int] = {
            "y": 31536000,
            "m": {
                1: 2678400, 2: 2419200, 3: 2678400, 4: 2592000,
                5: 2678400, 6: 2592000, 7: 2678400, 8: 2678400,
                9: 2592000, 10: 2678400, 11: 2592000, 12: 2678400},
            "d": 86400,
            "h": 3600,
            "mi": 60,
            "s": 1,
        }
    _SENTINEL_VALUE_: object = object()
    CENTRAL_EUROPEAN_TIMELINE:int = int(7200)

    def __init__(self):
        self.rawtime:float | int = 0
        self.drift:float | int = 0
        self.converter:int = 0
        self.min_clock_value:int = [1,1,1]  #has to do with whats the year, month, day lowest accepted value


        self.template:str = ['y', 'm', 'd', 'h', 'mi', 's']
        self.output:list = [None,None]
        self.epoch_type = AC if self.rawtime >= 0 else BC
    def __str__(self) -> dat :
        data, source = self.output

        Y, M, D, h, mi, s = data

        sec = int(s) if float(s).is_integer() else float(s)

        if self.converter != 0:
            #RAISE ISSUE
            pass

        # Determine self.epoch_type.name and adjusted values based on calendar mode and rawtime

        # Format string based on source type
        if source == "fulldat":
            return f"({Y:04}-{M:02}-{D:02} {h:02}:{mi:02}:{sec:02}){self.epoch_type.name}"
        elif source == "date":
            return f"({Y:04}-{M:02}-{D:02}) {self.epoch_type.name}"
        elif source == "time":
            return f"({h:02}:{mi:02}:{sec:02}) {self.epoch_type.name}"
        elif source == "year":
            return f"({Y:04}) {self.epoch_type.name}"
        elif source == "month":
            return f"({M:02}) {self.epoch_type.name}"
        elif source == "day":
            return f"({D:02}) {self.epoch_type.name}"
        elif source == "hour":
            return f"({h:02}) {self.epoch_type.name}"
        elif source == "minute":
            return f"({mi:02}) {self.epoch_type.name}"
        elif source == "second":
            return f"({sec:02}) {self.epoch_type.name}"
        else:
            return "No source Found"
    @classmethod
    def operand(cls, base_rawtime: dat | float | int,*, drift: dat | float | int = 0,reverse: bool = False,min_clock_value = [1,1,1]) :
        """
        Treat `base_rawtime` as seconds from the epoch, optionally subtracting drift.
        If `reverse=True`, flips the sign of `base_rawtime`.
        
        Returns a new dat object with the correct epoch and rawtime.
        """
        self = cls()
        self.min_clock_value = min_clock_value
        # If base_rawtime is a dat instance, extract its rawtime
        if isinstance(base_rawtime, dat):
            base_rawtime = base_rawtime.rawtime

        # 1) Convert drift to a float seconds value
        drift_sec = self.drift_converter(drift)

        # 2) Apply reverse flag if needed
        if reverse:
            base_rawtime = -base_rawtime

        # 3) Compute absolute rawtime: seconds since epoch
        absolute_rawtime = base_rawtime - drift_sec

        # 4) Determine epoch type (AC / BC) and magnitude for display
        if absolute_rawtime < 0:
            era = BC
            secs = abs(absolute_rawtime)
        else:
            era = AC
            secs = absolute_rawtime

        # 5) Convert seconds into full [Y, M, D, h, i, s]
        parts = self.convert_rawtime_to_date(secs)

        # 6) Fill instance and return
        self.rawtime = absolute_rawtime
        self.epoch_type = era
        self.output = [parts, "fulldat"]   
        self.drift = drift_sec
        dat_support.__init__(self) #always forget that operand thoesnt run on finalize_full_dat lol

        return self
    @classmethod
    def stamp(cls, input_value: list[int] | str = [0,1,1,0,0,0],input_template: list[str] | str = ['y', 'm', 'd', 'h', 'mi', 's'], epoch_type: EpochType = AC,*, drift: dat | float | int = 0,min_clock_value = [1,1,1]) :
        self = cls() # creates an instance
        self.min_clock_value = min_clock_value
        self.drift = self.drift_converter(drift)
        value, self.template = self.value_template_extractor(input_value,input_template)
        if len(value)>6 or len(self.template)>6:
            #RAISE ISSUE    
            pass
        if len(value) < len(self.template):
            #RAISE ISSUE
            pass
        return self.finalize_full_dat(value,epoch_type)
    @classmethod
    def datetime(cls, input_value: dat | list[int] | str = [0,1,1,0,0,0], epoch_type: EpochType = AC,*, drift: dat | float | int = 0,template_reverse = False,min_clock_value = [1,1,1]):
        """
        creates a dat object ussing the inputted values while autofilling in case of a lack of does,\n
        by default it follows the `[year,month,day,hour,minute,second]` sequence,\n
        if template_reverse is active, it will go from seconds to years instead 
        """
        self = cls() # creates an instance

        template = ['y', 'm', 'd', 'h', 'mi', 's'][::-1] if template_reverse else ['y', 'm', 'd', 'h', 'mi', 's']
        self.min_clock_value = min_clock_value
        self.drift = self.drift_converter(drift)
        value, self.template = self.value_template_extractor(input_value,template)

        if len(value)>6 or len(value) < 6:
            #RAISE ISSUE    
            pass
        return self.finalize_full_dat(value,epoch_type)
    @classmethod
    def current_time(cls,*, drift: float | int = 0) -> dat:
        """
        Returns the current real-world UTC time as [Y, m, d, h, i, s],\n
        adds the drift, `dat may be passed as an drift`
        """
        import time
        raw = time.localtime()  # returns struct_time in UTC
        now = [raw.tm_year, raw.tm_mon, raw.tm_mday, raw.tm_hour, raw.tm_min, raw.tm_sec]
        return dat.datetime(now,AC, drift = drift)
    #-----Support-Methods-------
    @classmethod
    def input_compiler(cls,rawtime:float | int = 0,template:tuple[str] = ('y', 'm', 'd', 'h', 'mi', 's'),drift:float | int = 0,output:list[list[int | bool | str]]= [None,None],*,chunk_input:str = _SENTINEL_VALUE_,min_clock_value = [1,1,1]):
        """
        providing uncorrect data might result in unexpected behaviour
        """
        self = cls()
        self.min_clock_value = min_clock_value
        if chunk_input == cls._SENTINEL_VALUE_:
    
            self.rawtime = rawtime
            self.drift= drift
            self.converter = 0
            
            self.template= template
            self.output= output
            self.epoch_type = AC if rawtime >= 0 else BC
        else:
            pieces = chunk_input.strip() 
            for item in ["(",")"," "]:
                pieces = pieces.replace(f"{item}","")
            pieces = pieces.split("|")
            self.rawtime = float(pieces[0])
            self.drift= float(pieces[1])
            temp_library:dict = {"fulldat":('y', 'm', 'd', 'h', 'mi', 's') }
            self.template= temp_library[pieces[2]] if pieces[2] in temp_library else pieces[2]
            
            self.output= ast.literal_eval(pieces[3])
            self.epoch_type = AC if rawtime >= 0 else BC

        return self      
    @property
    def export_compiler(self) -> str:
        "converts the important attributes of the dat object into a string, in such a format that input_compiler will understand it"
        temp_library:dict = {('y', 'm', 'd', 'h', 'mi', 's'):"fulldat"}
        template = temp_library[tuple(self.template)] if tuple(self.template) in temp_library else self.template
        return f"({self.rawtime} | {self.drift}| {template} | {self.output} | {self.epoch_type})"
    def finalize_full_dat(self, value:list[int], epoch_type: str = AC, output_type="fulldat",) -> dat :
        """
        standart method meant to convert a list of values into a dat object, considering their pre-set parameters
        """
        template_value_diccionary = {'y':0, 'm':1, 'd':1, 'h':0, 'mi':0, 's':0}
        for i in range(len(self.template)):
            for key in template_value_diccionary:
                if self.template[i] == key:
                    try:
                        template_value_diccionary[key] = value[i]
                        break
                    except IndexError:
                        break

        template_value_diccionary = self.normalize_full(template_value_diccionary)
        total_raw = self.convert_input_to_rawtime(template_value_diccionary)
        if epoch_type == BC:
            total_raw = -total_raw

        self.rawtime = total_raw
    
        parts = self.convert_rawtime_to_date(total_raw)
        self.output = [parts, output_type]
        dat_support.__init__(self)
        return self   
    def value_template_extractor(self, value: str | list[float | int], template: str) -> list[int] | list[str]:
        """
        if the value or the template are normal strings, it converts them into lists while trying to find their values
        if the value is a list[float | int], it just sends it back, same if the template is a list[str]
        """

        # handle people accidentally using brackets [] to store the full str value
        if (isinstance(value, list) and all(isinstance(x, str) for x in value)):
            value = value[0]

        # detect value if str
        if isinstance(value, str):
            NUMS = set("0123456789.")
            one_number: str = ""
            several_numbers: list[float] = []

            for val in value:
                if val in NUMS:
                    one_number += val
                else:
                    if one_number.strip():
                        several_numbers.append(float(one_number))
                    one_number = ""

            if one_number and all(nm in NUMS for nm in one_number):
                several_numbers.append(float(one_number))

            value: list[float] = several_numbers

        # detect value if list[float | int]
        elif not all(isinstance(item, (float, int)) for item in value):
            # RAISE ISSUE
            pass

        # detect template if str
        if isinstance(template, str):
            template = template.lower()
            tmp = []
            for item in self.TIME_UNITS:
                if item in template:
                    tmp.append(item)
                    template.replace(item, "")
            template = tmp

        # detect template if list[str]
        elif not all(isinstance(item, str) for item in template):
            # RAISE ISSUE
            pass

        if not value or not template:
            # RAISE ISSUE
            pass

        return [value, template]
    def convert_input_to_rawtime(self, template_value_diccionary: dict[str, float]) -> float:
        """
        Convert Y/m/d h:i:s into raw seconds and add drift. Uses exact calendar days (handles leap years)
        and assumes input dict fields may be floats. Relies on normalize_full producing integer Y,M,D,h,mi
        and float s (seconds).
        """

        def is_leap_year(y: int) -> bool:
            return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

        def days_since_epoch(Y: int, M: int, D: int) -> int:
            """
            Count days from year 0, month 1, day 1 up to Y/M/D (exclusive of the target day).
            Uses real month lengths and leap years. Returns an integer number of days.
            """
            mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            days = 0

            # count full years
            for y in range(0, Y):
                days += 366 if is_leap_year(y) else 365

            # count full months in final year
            for m in range(1, M):
                if m == 2:
                    days += 29 if is_leap_year(Y) else 28
                else:
                    days += mdays[m - 1]

            # days in current month: D is 1-based, so D-1 full days have passed
            return days + (D - 1)

        vals = template_value_diccionary

        # normalize_full should have been applied upstream, but guard anyway:
        Y = int(vals.get("y", 1))
        M = int(vals.get("m", 1))
        D = int(vals.get("d", 1))
        h = int(vals.get("h", 0))
        i = int(vals.get("mi", 0))
        s = float(vals.get("s", 0))

        total_days = days_since_epoch(Y, M, D)
        total = total_days * 86400 + h * 3600 + i * 60 + round(s,4)

        return float(total) + self.drift
    def drift_converter(self, drift: dat | float | int) -> float:
        """
        converts drifts into floats for more homogenous handling across methods
        """
        if isinstance(drift, (float, int)):
            return float(drift)
        elif isinstance(drift, dat):
            return drift.rawtime
        else:
            # RAISE ISSUE
            pass
    def normalize_full(self, full: dict[str, float]) -> dict[str, float]:
        """
        Robust normalization that:
        - Accepts floats in any field
        - Carries fractional parts precisely by converting fractional years/months to days
        using the accurate length of the specific year/month in question
        - Carries seconds->minutes->hours->days (seconds kept as float)
        - Returns ints for Y,M,D,h,mi and float for s
        """

        # local helpers
        def is_leap_year(y: int) -> bool:
            return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

        def days_in_month(year: int, month: int) -> int:
            if month == 2:
                return 29 if is_leap_year(year) else 28
            return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]

        def days_in_year(year: int) -> int:
            return 366 if is_leap_year(year) else 365

        # read inputs as floats
        Yf = float(full.get("y", 0.0))
        Mf = float(full.get("m", 0.0))
        Df = float(full.get("d", 0.0))
        hf = float(full.get("h", 0.0))
        mif = float(full.get("mi", 0.0))
        sf = float(full.get("s", 0.0))

        # 1) Carry seconds -> minutes
        mif += int(sf // 60)
        sf = sf % 60.0

        # 2) Carry minutes -> hours
        hf += int(mif // 60)
        mif = mif % 60.0

        # 3) Carry hours -> days
        Df += int(hf // 24)
        hf = hf % 24.0

        # 4) Deal with fractional years
        Y_int = int(Yf)
        fracY = Yf - Y_int
        if fracY != 0.0:
            Df += fracY * days_in_year(Y_int)
        Y = Y_int

        # 5) Normalize months
        Mf_total = Mf
        M_int = int(Mf_total)
        fracM = Mf_total - M_int

        if M_int <= 0:
            M_int = 1

        years_from_months, M = divmod(M_int - 1, 12)
        M += 1
        Y += int(years_from_months)

        # 6) Fractional month -> convert to days
        if fracM != 0.0:
            Df += fracM * days_in_month(Y, M)

        # 7) Add leftover integer days
        D_whole = int(Df)
        D_frac = Df - D_whole
        day = D_whole

        # normalize day
        while True:
            dim = days_in_month(Y, M)
            if day < 1:
                M -= 1
                if M < 1:
                    M = 12
                    Y -= 1
                day += days_in_month(Y, M)
            elif day > dim:
                day -= dim
                M += 1
                if M > 12:
                    M = 1
                    Y += 1
            else:
                break

        # 8) Convert fractional day into h, mi, s
        hf += D_frac * 24.0
        h_int = int(hf)
        hf_frac = hf - h_int
        mif += hf_frac * 60.0
        mi_int = int(mif)
        mif_frac = mif - mi_int
        sf += mif_frac * 60.0

        # normalize seconds/minutes/hours
        mi_int += int(sf // 60)
        sf = sf % 60.0
        h_int += int(mi_int // 60)
        mi_int = mi_int % 60
        day += int(h_int // 24)
        h_int = h_int % 24

        # final day normalization
        while True:
            dim = days_in_month(Y, M)
            if day < 1:
                M -= 1
                if M < 1:
                    M = 12
                    Y -= 1
                day += days_in_month(Y, M)
            elif day > dim:
                day -= dim
                M += 1
                if M > 12:
                    M = 1
                    Y += 1
            else:
                break

        return {
            "y": int(Y if Y >= self.min_clock_value[0] else 1),
            "m": int(M if M >= self.min_clock_value[1] else 1),
            "d": int(day if day >= self.min_clock_value[2] else 1),
            "h": int(h_int),
            "mi": int(mi_int),
            "s": float(sf),
        }
    def convert_rawtime_to_date(self, seconds: float | int) -> list:
        """
        Convert rawtime into [Y, m, d, h, i, s], accounting for drift.
        """

        def is_leap_year(y):
            return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

        days = int(seconds // 86400)
        rem = seconds % 86400
        Y = 0

        while True:
            year_days = 366 if is_leap_year(Y) else 365
            if days >= year_days:
                days -= year_days
                Y += 1
            else:
                break

        mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        M = 1
        while True:
            dim = 29 if (M == 2 and is_leap_year(Y)) else mdays[M - 1]
            if days >= dim:
                days -= dim
                M += 1
            else:
                break

        D = days + 1
        h = int(rem // 3600)
        rem %= 3600
        i = int(rem // 60)
        s = rem % 60

        return [Y, M, D, h, i, float(round(s,4))]


a = dat.current_time()

print(a)


