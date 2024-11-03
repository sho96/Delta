

#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <map>
#include <set>
#include <cmath>
#include <tuple>
#include <sstream>
#include <string>
#include <utility>
#include <type_traits>
#include <typeinfo>
#include <numeric>
#include <algorithm>

#include <cmath>
 #include <time.h>
 


template<typename K, typename V>
std::vector<K> getKeys(const std::map<K, V>& m) {
    std::vector<K> keys;
    keys.reserve(m.size()); // Optional: Reserve memory to improve performance
    for (const auto& pair : m) {
        keys.push_back(pair.first);
    }
    return keys;
}

template<typename Container>
void deleteAtIndex(Container& container, typename Container::size_type index) {
    if (index >= 0 && index < container.size()) {
        container.erase(container.begin() + index);
    } else {
        std::cout << "Index out of range" << std::endl;
    }
}

template<typename Container, typename T>
void removeByValue(Container& container, const T& value) {
    container.erase(std::remove(container.begin(), container.end(), value), container.end());
}

template<typename T>
std::vector<T> sliceVector(const std::vector<T>& vec, int sliceStart, int sliceEnd, int step=1) {
    // Adjust negative indices
    if (sliceStart < 0) sliceStart += vec.size();
    if (sliceEnd < 0) sliceEnd += vec.size();

    // Ensure indices are within bounds
    sliceStart = std::max(0, sliceStart);
    sliceEnd = std::min(static_cast<int>(vec.size()), sliceEnd);

    std::vector<T> result;
    if (step > 0) {
        for (int i = sliceStart; i < sliceEnd; i += step) {
            result.push_back(vec[i]);
        }
    } else if (step < 0) {
        for (int i = sliceStart; i > sliceEnd; i += step) {
            result.push_back(vec[i]);
        }
    }
    return result;
}
std::string sliceString(const std::string& str, int sliceStart, int sliceEnd, int step) {
    if (step == 0) {
        throw std::invalid_argument("Step cannot be zero.");
    }

    // Adjust negative indices
    if (sliceStart < 0) sliceStart += str.size();
    if (sliceEnd < 0) sliceEnd += str.size();

    // Ensure indices are within bounds
    if (step > 0) {
        sliceStart = std::max(0, sliceStart);
        sliceEnd = std::min(static_cast<int>(str.size()), sliceEnd);
    } else {
        sliceStart = std::min(static_cast<int>(str.size() - 1), sliceStart);
        sliceEnd = std::max(-1, sliceEnd);
    }

    std::string result;
    if (step > 0) {
        for (int i = sliceStart; i < sliceEnd; i += step) {
            result.push_back(str[i]);
        }
    } else if (step < 0) {
        for (int i = sliceStart; i > sliceEnd; i += step) {
            result.push_back(str[i]);
        }
    }
    return result;
}
std::vector<std::string> splitString(const std::string& str, char delimiter) {
    std::vector<std::string> result;
    std::stringstream ss(str);
    std::string item;
    while (std::getline(ss, item, delimiter)) {
        result.push_back(item);
    }
    return result;
}
std::vector<std::string> splitStringWithString(const std::string& str, const std::string& delimiter) {
    std::vector<std::string> result;
    std::string copy = str;
    std::string item;
    size_t pos = 0;
    while ((pos = copy.find(delimiter)) != std::string::npos) {
        item = copy.substr(0, pos);
        result.push_back(item);
        copy.erase(0, pos + delimiter.length());
    }
    result.push_back(copy);
    return result;
}
std::vector<char> splitStringToChars(const std::string& str) {
    std::vector<char> result(str.begin(), str.end());
    return result;
}
char maxCharInString(const std::string &str)
{
    char maxChar = '\0';
    for (char c : str)
    {
        if (c > maxChar)
        {
            maxChar = c;
        }
    }
    return maxChar;
}
std::string string_join(const std::vector<std::string> &vec, const std::string &delimiter)
{
    std::string result = "";
    for (const auto &item : vec)
    {
        result += item + delimiter;
    }
    result.resize(result.size() - delimiter.size());
    return result;
}
std::string string_strip(const std::string &str, const std::string &chars)
{
    std::string result = str;
    result.erase(0, result.find_first_not_of(chars));
    result.erase(result.find_last_not_of(chars) + 1);
    return result;
}
std::string string_toupper(const std::string &str)
{
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::toupper);
    return result;
}
std::string string_tolower(const std::string &str)
{
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}
std::string string_replace(const std::string &str, const std::string &from, const std::string &to)
{
    std::string result = str;
    size_t start_pos = 0;
    while ((start_pos = result.find(from, start_pos)) != std::string::npos)
    {
        result.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
    return result;
}
int string_count(const std::string& str, const std::string& sub)
{
	if (sub.length() == 0) return 0;
	int count = 0;
	for (size_t offset = str.find(sub); offset != std::string::npos;
	offset = str.find(sub, offset + sub.length()))
	{
		++count;
	}
	return count;
}
int string_count_char(std::string s, char c) {
    int count = 0;

    for (int i = 0; i < s.size(); i++)
        if (s[i] == c) count++;

    return count;
}
bool string_isdigit(const std::string& str) {
    for (char ch : str) {
        if (!std::isdigit(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isalpha(const std::string& str) {
    for (char ch : str) {
        if (!std::isalpha(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isalnum(const std::string& str) {
    for (char ch : str) {
        if (!std::isalnum(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isascii(const std::string& str) {
    for (char ch : str) {
        if (!(ch >= 0 && ch <= 127)) {
            return false;
        }
    }
    return true;
}
bool string_isspace(const std::string& str) {
    for (char ch : str) {
        if (!std::isspace(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_isupper(const std::string& str) {
    for (char ch : str) {
        if (!std::isupper(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
bool string_islower(const std::string& str) {
    for (char ch : str) {
        if (!std::islower(static_cast<unsigned char>(ch))) {
            return false;
        }
    }
    return true;
}
std::string userInput(std::string prompt="") {
    std::cout << prompt;
    std::string input;
    std::getline(std::cin, input);
    return input;
}
template <typename T, typename... Types>
std::string createJoinedStr(T var1, Types... var2)
{
    std::stringstream ss;
    ss << var1;
    (ss << ... << var2);
    return ss.str();
}
template <typename T>
std::vector<T> concatVec(std::vector<T> vec1, std::vector<T> vec2)
{
    vec1.insert(vec1.end(), vec2.begin(), vec2.end());
    return vec1;
}
template <typename T>
std::set<T> concatSet(std::set<T> set1, std::set<T> set2){
    set1.insert(set2.begin(), set2.end());
    return set1;
}
template <typename T, typename U>
std::map<T, U> concatMap(std::map<T, U> map1, std::map<T, U> map2){
    map1.insert(map2.begin(), map2.end());
    return map1;
}
template <typename T>
std::vector<T> repeatVec(std::vector<T> vec, int count) {
    std::vector<T> result;
    for (int i = 0; i < count; i++) {
        result.insert(result.end(), vec.begin(), vec.end());
    }
    return result;
}



// Forward declarations of conversion functions
template <typename V>
std::string vec2str(const std::vector<V> &vec);

template <typename K, typename V>
std::string map2str(const std::map<K, V> &map);

template <typename V>
std::string set2str(const std::set<V> &set);

template <typename... Args>
std::string tuple2str(const std::tuple<Args...> &tup);

// Specialization for std::string
std::string valueToString(const std::string &value)
{
    return "\"" + value + "\"";
}

// Specialization for bool
std::string valueToString(const bool &value)
{
    return value ? "true" : "false";
}

// Specialization for std::tuple
template <typename... Args>
std::string valueToString(const std::tuple<Args...> &tup)
{
    return tuple2str(tup);
}

// Specialization for std::vector
template <typename V>
std::string valueToString(const std::vector<V> &vec)
{
    return vec2str(vec);
}

// Specialization for std::map
template <typename K, typename V>
std::string valueToString(const std::map<K, V> &map)
{
    return map2str(map);
}

// Specialization for std::set
template <typename V>
std::string valueToString(const std::set<V> &set)
{
    return set2str(set);
}

// Generic valueToString template
template <typename T>
std::string valueToString(const T &value)
{
    std::ostringstream oss;
    oss << value;
    return oss.str();
}

// Conversion functions
template <typename V>
std::string vec2str(const std::vector<V> &vec)
{
    std::string result = "[";
    for (const auto &item : vec)
    {
        result += valueToString(item) + ", ";
    }
    if (!vec.empty())
        result.resize(result.size() - 2); // Remove last ", "
    result += "]";
    return result;
}

template <typename K, typename V>
std::string map2str(const std::map<K, V> &map)
{
    std::string result = "{";
    for (const auto &[key, value] : map)
    {
        result += valueToString(key) + ": ";
        result += valueToString(value) + ", ";
    }
    if (!map.empty())
        result.resize(result.size() - 2); // Remove last ", "
    result += "}";
    return result;
}

template <typename V>
std::string set2str(const std::set<V> &set)
{
    std::string result = "{";
    for (const auto &item : set)
    {
        result += valueToString(item) + ", ";
    }
    if (!set.empty())
        result.resize(result.size() - 2); // Remove last ", "
    result += "}";
    return result;
}

// Helper function to convert a tuple to a string
template <typename Tuple, std::size_t... Is>
std::string tuple2str_impl(const Tuple &tup, std::index_sequence<Is...>)
{
    std::string result = "(";
    ((result += valueToString(std::get<Is>(tup)) + ", "), ...);
    if constexpr (sizeof...(Is) > 0)
        result.resize(result.size() - 2); // Remove last ", "
    result += ")";
    return result;
}

template <typename... Args>
std::string tuple2str(const std::tuple<Args...> &tup)
{
    return tuple2str_impl(tup, std::index_sequence_for<Args...>{});
}
void name ( int arg1 ,  std::string arg2 ) {
 ( std::cout <<  arg2   <<  std::endl ) ;
 ( std::cout <<  arg1   <<  std::endl ) ;
 ( std::cout <<  std::to_string( arg1 )   <<  std::endl ) ;
 
} 

int main() {
;
 ;
 std::string string = "some random string" ;
 int integer = 123 ;
 double decimal = 1.23 ;
 char chr2 = 123 ;
 bool isTrue = true ;
 std::tuple< int , double , bool > s = std::make_tuple( 1 , 1.23 , false ) ;
 std::vector< double > l = { 0.123 , 0.234 , 0.345 } ;
 std::map< std::string ,  int > d = { { "one" , 1 } , { "two" , 2 } , { "three" , 3 } } ;
 std::vector< std::tuple< std::string , int , int > > items = { std::make_tuple( "kahimochi" , 4 , 500 ) , std::make_tuple( "pets" , 20 , 215 ) , std::make_tuple( "paper clips" , 50 , 100 ) } ;
 ;
 int x = 0 ;
 if( x <= 1  && x >= - 10   || x >= 10  && x <= 20   ) {
 ( std::cout <<  "x is in range!!"   <<  std::endl ) ;
 
} else {
 if( x == 100 ) {
 ( std::cout <<  "x is 100"   <<  std::endl ) ;
 
} else {
 ( std::cout <<  "x is not in range..."   <<  std::endl ) ;
 
} ;
 
} ;
 for(int  i =  0 ;  i  <  10 ;  i  +=  1 ) {
 ( std::cout <<  i   <<  std::endl ) ;
 
} ;
 for( const std::tuple< std::string , int , int > item  :  items ) {
 ( std::cout <<  std::get< 0 >( item )   <<  std::endl ) ;
 ( std::cout <<  std::get< 1 >( item )   <<  std::endl ) ;
 ( std::cout <<  std::get< 2 >( item )   <<  std::endl ) ;
 
} ;
 while( x < 1000 ) {
 x += 1 ;
 
} ;
 switch ( x ) {
 case 1 :
 ( std::cout <<  "x is 1"   <<  std::endl ) ;
 break;
 case 2 :
 ( std::cout <<  "x is 2"   <<  std::endl ) ;
 break;
 default:
 ( std::cout <<  "x is not 1 or 2"   <<  std::endl ) ;
 break;
 }
 ;
 ( std::cout <<  createJoinedStr( "The value of x is " , x )   <<  std::endl ) ;
 ( std::cout <<  "Hello Delta!!"   <<  "" ) ;
 
    return 0;
}
