#include <libhandler.h>

LH_DEFINE_EFFECT1(exn, raise)

LH_DEFINE_VOIDOP1(exn, raise, lh_string)

lh_value id(lh_value arg) {
  return arg;
}

lh_value id_raise(lh_value arg) {
  exn_raise("an error message from 'id_raise'");
  return arg;
}

lh_value exn_handle(lh_value(*action)(lh_value), lh_value arg) {

  return lh_handle(&exn_def, lh_value_null, action, arg);

}

int main()
{
	lh_value res1 = exn_handle(id, lh_value_long(42));     
}
