// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <string>

#include "awkward/type/UnknownType.h"

namespace awkward {
  std::string UnknownType::tostring_part(std::string indent, std::string pre, std::string post) const {
    return indent + pre + "???" + post;
  }

  const std::shared_ptr<Type> UnknownType::shallow_copy() const {
    return std::shared_ptr<Type>(new UnknownType());
  }

  bool UnknownType::equal(std::shared_ptr<Type> other) const {
    return true;
  }
}
